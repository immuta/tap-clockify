"""Stream type classes for tap-clockify."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_clockify.client import ClockifyStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class ClientsStream(ClockifyStream):
    name = "clients"
    primary_keys = ["id"]
    path = "/clients"
    schema_filepath = SCHEMAS_DIR / "clients.json"


class ProjectsStream(ClockifyStream):
    name = "projects"
    primary_keys = ["id"]
    path = "/projects"
    schema_filepath = SCHEMAS_DIR / "projects.json"

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
    schema_filepath = SCHEMAS_DIR / "tags.json"


class UsersStream(ClockifyStream):
    name = "users"
    primary_keys = ["id"]
    path = "/users"
    schema_filepath = SCHEMAS_DIR / "users.json"

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
    schema_filepath = SCHEMAS_DIR / "tasks.json"


class TimeEntriesStream(ClockifyStream):
    name = "time_entries"
    primary_keys = ["id"]
    path = "/user/{user_id}/time-entries"
    parent_stream_type = UsersStream
    replication_key = "started_at"
    ignore_parent_replication_key = True
    schema_filepath = SCHEMAS_DIR / "time_entries.json"

    def post_process(self, row: dict, context: Optional[dict]) -> dict:
        row["started_at"] = row["timeInterval"]["start"]
        return row


class WorkspacesStream(ClockifyStream):
    name = "workspaces"
    primary_keys = ["id"]
    path = "/workspaces"
    schema_filepath = SCHEMAS_DIR / "workspaces.json"

    @property
    def url_base(self):
        return f"https://api.clockify.me/api/v1"
