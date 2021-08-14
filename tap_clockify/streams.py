"""Stream type classes for tap-clockify."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_clockify import schemas
from tap_clockify.client import ClockifyStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ClientsStream(ClockifyStream):
    name = "clients"
    primary_keys = ["id"]
    path = "/clients"
    schema = schemas.clients


class ProjectsStream(ClockifyStream):
    name = "projects"
    primary_keys = ["id"]
    path = "/projects"
    schema = schemas.projects

    def get_records(self, context: Optional[dict]):
        "Overwrite default method to return both the record and child context."
        for row in self.request_records(context):
            row = self.post_process(row, context)
            child_context = {"project_id": row["id"]}
            yield (row, child_context)


class TagsStream(ClockifyStream):
    name = "tags"
    primary_keys = ["id"]
    path = "/tags"
    schema = schemas.tags


class UsersStream(ClockifyStream):
    name = "users"
    primary_keys = ["id"]
    path = "/users"
    schema = schemas.users

    def get_records(self, context: Optional[dict]):
        "Overwrite default method to return both the record and child context."
        for row in self.request_records(context):
            row = self.post_process(row, context)
            child_context = {"user_id": row["id"]}
            yield (row, child_context)


class TasksStream(ClockifyStream):
    name = "tasks"
    primary_keys = ["id"]
    path = "/projects/{project_id}/tasks"
    parent_stream_type = ProjectsStream
    ignore_parent_replication_key = True
    schema = schemas.tasks


class TimeEntriesStream(ClockifyStream):
    name = "time_entries"
    primary_keys = ["id"]
    path = "/user/{user_id}/time-entries"
    parent_stream_type = UsersStream
    replication_key = "started_at"
    ignore_parent_replication_key = True
    schema = schemas.time_entries

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        row["started_at"] = row["timeInterval"]["start"]
        return row


class WorkspacesStream(ClockifyStream):
    name = "workspaces"
    primary_keys = ["id"]
    path = "/workspaces"
    schema = schemas.workspaces

    @property
    def url_base(self):
        return f"https://api.clockify.me/api/v1"
