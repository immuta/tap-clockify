from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("name", th.StringType),
    th.Property("email", th.StringType),
    th.Property("profilePicture", th.StringType),
    th.Property("activeWorkspace", th.StringType),
    th.Property("defaultWorkspace", th.StringType),
    th.Property("status", th.StringType),
    th.Property(
        "memberships",
        th.ArrayType(
            th.ObjectType(
                th.Property("userId", th.StringType),
                th.Property(
                    "hourlyRate",
                    th.ObjectType(
                        th.Property("amount", th.NumberType),
                        th.Property("currency", th.StringType),
                    ),
                ),
                th.Property("targetId", th.StringType),
                th.Property("membershipType", th.StringType),
                th.Property("membershipStatus", th.StringType),
            )
        ),
    ),
).to_dict()
