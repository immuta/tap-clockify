import singer

from tap_clockify.streams.base import BaseStream
from tap_clockify.streams import cache as stream_cache


LOGGER = singer.get_logger()  # noqa


class TagStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'tags'
    KEY_PROPERTIES = ['id']

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"/workspaces/{self.config['workspace']}/tags"