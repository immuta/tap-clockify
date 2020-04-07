import singer

from tap_clockify.streams.base import TimeRangeByObjectStream
from tap_clockify.streams import cache as stream_cache


LOGGER = singer.get_logger()  # noqa


class TimeEntryStream(TimeRangeByObjectStream):
    API_METHOD = "GET"
    TABLE = "time_entries"
    KEY_PROPERTIES = ["id"]
    REPLACEMENT_STRING = "<VAR>"

    CACHE_RESULTS = True

    def get_object_list(self):
        url = self.get_url_base() + f"/workspaces/{self.config['workspace']}/users"
        api_method = "GET"
        params = {"page-size": 500, "memberships": "NONE"}
        results = self.client.make_request(url, api_method, params=params)
        return [r["id"] for r in results]

    @property
    def path(self):
        return f"/workspaces/{self.config['workspace']}/user/<VAR>/time-entries"