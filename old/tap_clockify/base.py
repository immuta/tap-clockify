import inspect
import os.path
import pytz
import singer
import tap_clockify.cache as stream_cache

from datetime import timedelta, datetime

from tap_clockify.config import get_config_start_date
from tap_clockify.state import incorporate, save_state, get_last_record_value_for_table


LOGGER = singer.get_logger()


class BaseStream:
    # GLOBAL PROPERTIES
    TABLE = None
    KEY_PROPERTIES = ["id"]
    API_METHOD = "GET"
    REQUIRES = []
    CACHE_RESULTS = False
    path = ""

    def __init__(self, config, state, catalog, client):
        self.config = config
        self.state = state
        self.catalog = catalog
        self.client = client
        self.substreams = []

    def get_url_base(self):
        return "https://api.clockify.me/api/v1"

    def get_url(self):
        base = self.get_url_base()
        return f"{base}{self.path}"

    def get_params(self, page=1):
        return {"page-size": 100, "page": page}

    def get_class_path(self):
        return os.path.dirname(inspect.getfile(self.__class__))

    def load_schema_by_name(self, name):
        return singer.utils.load_json(
            os.path.normpath(
                os.path.join(self.get_class_path(), "schemas/{}.json".format(name))
            )
        )

    def get_schema(self):
        return self.load_schema_by_name(self.TABLE)

    def get_stream_data(self, result):
        """Given a result set, return the data
        to be persisted for this stream.
        """
        return [self.transform_record(record) for record in result]

    @classmethod
    def requirements_met(cls, catalog):
        selected_streams = [s.stream for s in catalog.streams if is_selected(s)]

        return set(cls.REQUIRES).issubset(selected_streams)

    @classmethod
    def matches_catalog(cls, stream_catalog):
        return stream_catalog.stream == cls.TABLE

    def generate_catalog(self, selected_by_default=True):
        schema = self.get_schema()
        mdata = singer.metadata.new()

        mdata = singer.metadata.write(mdata, (), "inclusion", "available")
        mdata = singer.metadata.write(
            mdata, (), "selected-by-default", selected_by_default
        )

        for field_name in schema.get("properties").keys():
            inclusion = "available"

            if field_name in self.KEY_PROPERTIES:
                inclusion = "automatic"

            mdata = singer.metadata.write(
                mdata, ("properties", field_name), "inclusion", inclusion
            )
            mdata = singer.metadata.write(
                mdata,
                ("properties", field_name),
                "selected-by-default",
                selected_by_default,
            )

        return [
            {
                "tap_stream_id": self.TABLE,
                "stream": self.TABLE,
                "key_properties": self.KEY_PROPERTIES,
                "schema": self.get_schema(),
                "metadata": singer.metadata.to_list(mdata),
            }
        ]

    def transform_record(self, record):
        with singer.Transformer() as tx:
            metadata = {}

            if self.catalog.metadata is not None:
                metadata = singer.metadata.to_map(self.catalog.metadata)

            return tx.transform(record, self.catalog.schema.to_dict(), metadata)

    def get_catalog_keys(self):
        return list(self.catalog.schema.properties.keys())

    def write_schema(self):
        singer.write_schema(
            self.catalog.stream,
            self.catalog.schema.to_dict(),
            key_properties=self.catalog.key_properties,
        )

    def sync(self):
        LOGGER.info(
            "Syncing stream {} with {}".format(
                self.catalog.tap_stream_id, self.__class__.__name__
            )
        )

        self.write_schema()

        return self.sync_data()

    def sync_data(self):
        table = self.TABLE

        LOGGER.info("Syncing data for %s", table)

        url = self.get_url()
        params = self.get_params()
        resources = self.sync_paginated(url, params)

        if self.CACHE_RESULTS:
            stream_cache.add(table, resources)
            LOGGER.info("Added %s %s to cache", len(resources), table)

        LOGGER.info("Reached end of stream, moving on.")
        save_state(self.state)
        return self.state

    def sync_paginated(self, url, params):
        table = self.TABLE
        _next = True
        page = 1

        all_resources = []
        # Clockify returns an array of data, without pagination metadata
        # Should iterate if number of results > page size
        while _next is not None:
            result = self.client.make_request(url, self.API_METHOD, params=params)
            data = self.get_stream_data(result)

            with singer.metrics.record_counter(endpoint=table) as counter:
                singer.write_records(table, data)
                counter.increment(len(data))
                all_resources.extend(data)

            LOGGER.info("Synced page %s for %s", page, self.TABLE)
            params["page"] = params["page"] + 1
            if len(data) < params["page-size"]:
                _next = None
        return all_resources


def is_selected(stream_catalog):
    metadata = singer.metadata.to_map(stream_catalog.metadata)
    stream_metadata = metadata.get((), {})

    inclusion = stream_metadata.get("inclusion")

    if stream_metadata.get("selected") is not None:
        selected = stream_metadata.get("selected")
    else:
        selected = stream_metadata.get("selected-by-default")

    if inclusion == "unsupported":
        return False

    elif selected is not None:
        return selected

    return inclusion == "automatic"


class TimeRangeByObjectStream(BaseStream):
    """Stream that retrieves data based on a time range, and
    iterates over a certain dimension, such as <userId> or
    <projectId>.
    """

    RANGE_FIELD = "start"
    REPLACEMENT_STRING = "<VAR>"

    def get_params(self, start, end, page=1):
        return {
            self.RANGE_FIELD: start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "page": 1,
            "page-size": 250,
        }

    def get_object_list(self):
        return []

    def sync_data(self):
        table = self.TABLE
        object_list = self.get_object_list()

        start_date = get_last_record_value_for_table(self.state, table)
        if start_date is None:
            start_date = get_config_start_date(self.config)
        end_date = datetime.now(pytz.utc)

        all_resources = self.sync_data_for_period(start_date, end_date, object_list)

        if self.CACHE_RESULTS:
            stream_cache.add(table, all_resources)
            LOGGER.info("Added %s %s to cache", len(all_resources), table)

        return self.state

    def sync_data_for_period(self, start_date, end_date, object_list):
        table = self.TABLE

        LOGGER.info(
            "Syncing data from %s to %s", start_date.isoformat(), end_date.isoformat()
        )

        for obj in object_list:
            params = self.get_params(start_date, end_date)
            url = self.get_url().replace(self.REPLACEMENT_STRING, obj)
            res = self.sync_paginated(url, params)

        self.state = incorporate(
            self.state, table, self.RANGE_FIELD, end_date.isoformat()
        )

        save_state(self.state)
        return res
