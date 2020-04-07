import math
import pytz
import singer
import singer.utils
import singer.metrics

from datetime import timedelta, datetime

from tap_clockify.streams import cache as stream_cache
from tap_clockify.config import get_config_start_date
from tap_clockify.state import incorporate, save_state, \
    get_last_record_value_for_table

from tap_framework.streams import BaseStream as base


LOGGER = singer.get_logger()


class BaseStream(base):
    KEY_PROPERTIES = ["id"]
    CACHE_RESULTS = False
    path = ""

    def get_url_base(self):
        return f"https://api.clockify.me/api/v1"

    def get_url(self):
        base = self.get_url_base()
        return f"{base}{self.path}"

    def get_params(self, page=1):
        return {"page-size": 100, "page": page}

    def sync_data(self):
        table = self.TABLE

        LOGGER.info("Syncing data for {}".format(table))

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
            if len(data) < params["page-size"]:
                _next = None
        return all_resources

    def get_stream_data(self, result):
        return [
            self.transform_record(record)
            for record in result
        ]


class TimeRangeByObjectStream(BaseStream):
    """Stream that retrieves data based on a time range, and
    iterates over a certain dimension, such as <userId> or
    <projectId>.
    """
    RANGE_FIELD = "start"
    REPLACEMENT_STRING = "<VAR>"

    def get_params(self, start, end):
        return {
            self.RANGE_FIELD: start.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "end": end.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "page-size": 100
        }

    def get_object_list(self):
        return []

    def sync_data(self):
        table = self.TABLE
        object_list = self.get_object_list()

        date = get_last_record_value_for_table(self.state, table)
        if date is None:
            date = get_config_start_date(self.config)

        interval = timedelta(days=7)

        all_resources = []
        while date < datetime.now(pytz.utc):
            res = self.sync_data_for_period(date, interval, object_list)
            all_resources.extend(res)
            date = date + interval

        if self.CACHE_RESULTS:
            stream_cache.add(table, all_resources)
            LOGGER.info("Added %s %s to cache", len(all_resources), table)

        return self.state

    def sync_data_for_period(self, date, interval, object_list):
        table = self.TABLE

        updated_after = date
        updated_before = updated_after + interval

        LOGGER.info(
            "Syncing data from %s to %s",
            updated_after.isoformat(),
            updated_before.isoformat())
        
        for obj in object_list:
            params = self.get_params(updated_after, updated_before)
            url = self.get_url().replace(self.REPLACEMENT_STRING, obj)
            res = self.sync_paginated(url, params)

        self.state = incorporate(self.state,
                                 table,
                                 self.RANGE_FIELD,
                                 date.isoformat())

        save_state(self.state)
        return res