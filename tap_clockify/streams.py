"""Stream type classes for tap-clockify."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_clockify.client import ClockifyStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


# class UsersStream(ClockifyStream):
#     """Define custom stream."""
#     name = "users"
#     path = "/users"
#     primary_keys = ["id"]
#     replication_key = None
#     # Optionally, you may also use `schema_filepath` in place of `schema`:
#     # schema_filepath = SCHEMAS_DIR / "users.json"
#     schema = th.PropertiesList(
#         th.Property("name", th.StringType),
#         th.Property("id", th.StringType),
#         th.Property("age", th.IntegerType),
#         th.Property("email", th.StringType),
#         th.Property("street", th.StringType),
#         th.Property("city", th.StringType),
#         th.Property("state", th.StringType),
#         th.Property("zip", th.StringType),
#     ).to_dict()


# class GroupsStream(ClockifyStream):
#     """Define custom stream."""
#     name = "groups"
#     path = "/groups"
#     primary_keys = ["id"]
#     replication_key = "modified"
#     schema = th.PropertiesList(
#         th.Property("name", th.StringType),
#         th.Property("id", th.StringType),
#         th.Property("modified", th.DateTimeType),
#     ).to_dict()



class ClientsStream(ClockifyStream):
    name = "clients"
    primary_keys = ["id"]
    path = "/clients"
    schema_filepath = SCHEMAS_DIR / "clients.json"


class ProjectsStream(ClockifyStream):
    name = "projects"
    primary_keys = ["id"]
    path =  "/projects"
    schema_filepath = SCHEMAS_DIR / "projects.json"


class TagsStream(ClockifyStream):
    name = "tags"
    primary_keys = ["id"]
    path =  "/tags"
    schema_filepath = SCHEMAS_DIR / "tags.json"


class UsersStream(ClockifyStream):
    name = "users"
    primary_keys = ["id"]
    path = "/users"
    schema_filepath = SCHEMAS_DIR / "users.json"


class WorkspacesStream(ClockifyStream):
    name = "workspaces"
    primary_keys = ["id"]
    path = "/workspaces"
    schema_filepath = SCHEMAS_DIR / "workspaces.json"


# class TaskStream(TimeRangeByObjectStream):
#     name = "tasks"
#     primary_keys = ["id"]
#     REPLACEMENT_STRING = "<VAR>"
#     path =  "/projects/<VAR>/tasks"

#     def get_object_list(self):
#         url = self.get_url_base() + "/projects"
#         api_method = "GET"
#         params = {"page-size": 500}
#         results = self.client.make_request(url, api_method, params=params)
#         return [r["id"] for r in results]


# class TimeEntryStream(TimeRangeByObjectStream):
#     name = "time_entries"
#     primary_keys = ["id"]
#     REPLACEMENT_STRING = "<VAR>"
#     path =  "/user/<VAR>/time-entries"


#     def get_object_list(self):
#         url = self.get_url_base() + "/users"
#         api_method = "GET"
#         params = {"page-size": 500, "memberships": "NONE"}
#         results = self.client.make_request(url, api_method, params=params)
#         return [r["id"] for r in results]
