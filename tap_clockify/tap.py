"""Clockify tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

from tap_clockify.streams import (
    ClientsStream,
    ProjectsStream,
    TagsStream,
    TasksStream,
    TimeEntriesStream,
    UsersStream,
    WorkspacesStream,
)

STREAM_TYPES = [
    ClientsStream,
    ProjectsStream,
    TagsStream,
    TasksStream,
    TimeEntriesStream,
    UsersStream,
    WorkspacesStream,
]


class TapClockify(Tap):
    """Clockify tap class."""

    name = "tap-clockify"

    config_jsonschema = th.PropertiesList(
        th.Property("api_key", th.StringType, required=True),
        th.Property("workspace", th.StringType, required=True),
        th.Property("start_date", th.DateTimeType),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
