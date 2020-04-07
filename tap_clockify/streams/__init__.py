from tap_clockify.streams.clients import ClientStream
from tap_clockify.streams.projects import ProjectStream
from tap_clockify.streams.tags import TagStream
from tap_clockify.streams.tasks import TaskStream
from tap_clockify.streams.time_entries import TimeEntryStream
from tap_clockify.streams.users import UserStream
from tap_clockify.streams.workspaces import WorkspaceStream


AVAILABLE_STREAMS = [
    ClientStream,
    ProjectStream,
    TagStream,
    UserStream,
    TaskStream,
    TimeEntryStream,
    WorkspaceStream
]

__all__ = [
    "ClientStream",
    "ProjectStream",
    "TagStream",
    "TaskStream",
    "TimeEntryStream",
    "UserStream",
    "WorkspaceStream",
]