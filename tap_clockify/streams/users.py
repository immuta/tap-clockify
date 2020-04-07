import singer

from tap_clockify.streams.base import BaseStream
from tap_clockify.streams import cache as stream_cache


LOGGER = singer.get_logger()  # noqa


class UserStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'users'
    KEY_PROPERTIES = ['id']

    CACHE_RESULTS = True

    def get_params(self, page=1):
        return {
            "page-size": 100,
            "page": page,
            "memberships": "ALL"}

    @property
    def path(self):
        return f"/workspace/{self.config['workspace']}/users"