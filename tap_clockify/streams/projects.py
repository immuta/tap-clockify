import singer

from tap_clockify.streams.base import BaseStream
from tap_clockify.streams import cache as stream_cache


LOGGER = singer.get_logger()  # noqa


class ProjectStream(BaseStream):
    API_METHOD = 'GET'
    TABLE = 'projects'
    KEY_PROPERTIES = ['id']

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"/workspaces/{self.config['workspace']}/projects"