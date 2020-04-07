import singer

from tap_clockify.streams.base import BaseStream
from tap_clockify.streams import cache as stream_cache


LOGGER = singer.get_logger()  # noqa


class WorkspaceStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'workspaces'
    KEY_PROPERTIES = ['id']

    CACHE_RESULTS = True

    @property
    def path(self):
        return '/workspaces'