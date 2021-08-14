from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("projectId", th.StringType),
    th.Property("assigneeId", th.StringType),
    th.Property("name", th.StringType),
    th.Property("duration", th.StringType),
    th.Property("estimate", th.StringType),
    th.Property("status", th.StringType),
    th.Property("assigneeIds", th.ArrayType(th.StringType)),
).to_dict()
