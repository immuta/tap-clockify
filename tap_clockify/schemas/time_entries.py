from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("started_at", th.DateTimeType),
    th.Property("userId", th.StringType),
    th.Property("projectId", th.StringType),
    th.Property("taskId", th.StringType),
    th.Property("workspaceId", th.StringType),
    th.Property("billable", th.BooleanType),
    th.Property("description", th.StringType),
    th.Property("isLocked", th.BooleanType),
    th.Property("customFieldValues", th.ArrayType(th.StringType)),
    th.Property("tagIds", th.ArrayType(th.StringType)),
    th.Property(
        "timeInterval",
        th.ObjectType(
            th.Property("duration", th.StringType),
            th.Property("end", th.StringType),
            th.Property("start", th.StringType),
        ),
    ),
).to_dict()
