import singer

from tap_clockify.base import BaseStream, TimeRangeByObjectStream


LOGGER = singer.get_logger()


class ClientStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "clients"
    KEY_PROPERTIES = ["id"]

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"/workspaces/{self.config['workspace']}/clients"


class ProjectStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "projects"
    KEY_PROPERTIES = ["id"]

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"/workspaces/{self.config['workspace']}/projects"


class TagStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "tags"
    KEY_PROPERTIES = ["id"]

    CACHE_RESULTS = True

    @property
    def path(self):
        return f"/workspaces/{self.config['workspace']}/tags"


class UserStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "users"
    KEY_PROPERTIES = ["id"]

    CACHE_RESULTS = True

    def get_params(self, page=1):
        return {"page-size": 100, "page": page, "memberships": "ALL"}

    @property
    def path(self):
        return f"/workspace/{self.config['workspace']}/users"


class WorkspaceStream(BaseStream):
    API_METHOD = "GET"
    TABLE = "workspaces"
    KEY_PROPERTIES = ["id"]

    CACHE_RESULTS = True

    @property
    def path(self):
        return "/workspaces"


class TaskStream(TimeRangeByObjectStream):
    API_METHOD = "GET"
    TABLE = "tasks"
    KEY_PROPERTIES = ["id"]
    REPLACEMENT_STRING = "<VAR>"

    CACHE_RESULTS = True

    def get_object_list(self):
        url = self.get_url_base() + f"/workspaces/{self.config['workspace']}/projects"
        api_method = "GET"
        params = {"page-size": 500}
        results = self.client.make_request(url, api_method, params=params)
        return [r["id"] for r in results]

    @property
    def path(self):
        return f"/workspaces/{self.config['workspace']}/projects/<VAR>/tasks"


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


AVAILABLE_STREAMS = [
    ClientStream,
    ProjectStream,
    TagStream,
    UserStream,
    TaskStream,
    TimeEntryStream,
    WorkspaceStream,
]
