from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("name", th.StringType),
    th.Property("clientId", th.StringType),
    th.Property("workspaceId", th.StringType),
    th.Property("billable", th.BooleanType),
    th.Property("archived", th.BooleanType),
    th.Property("duration", th.StringType),
    th.Property("clientName", th.StringType),
    th.Property("note", th.StringType),
    th.Property("template", th.BooleanType),
    th.Property("public", th.BooleanType),
    th.Property("color", th.StringType),
    th.Property(
        "estimate",
        th.ObjectType(
            th.Property("estimate", th.StringType),
            th.Property("type", th.StringType),
        ),
    ),
    th.Property(
        "hourlyRate",
        th.ObjectType(
            th.Property("amount", th.NumberType),
            th.Property("currency", th.StringType),
        ),
    ),
).to_dict()
