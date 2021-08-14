from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("name", th.StringType),
    th.Property("workspaceId", th.StringType),
    th.Property("archived", th.BooleanType),
).to_dict()
