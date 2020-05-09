from tap_clockify.streams.streams import \
    ClientStream,    \
    ProjectStream,   \
    TagStream,       \
    UserStream,      \
    TaskStream,      \
    TimeEntryStream, \
    WorkspaceStream


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