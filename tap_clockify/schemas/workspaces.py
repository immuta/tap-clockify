from singer_sdk import typing as th

schema = th.PropertiesList(
    th.Property("id", th.StringType),
    th.Property("name", th.StringType),
    th.Property("imageUrl", th.StringType),
    th.Property(
        "hourlyRate",
        th.ObjectType(
            th.Property("amount", th.IntegerType),
            th.Property("currency", th.StringType),
        ),
    ),
    th.Property(
        "workspaceSettings",
        th.ObjectType(
            th.Property("adminOnlyPages", th.ArrayType(th.StringType)),
            th.Property(
                "automaticLock",
                th.ObjectType(
                    th.Property("changeDay", th.StringType),
                    th.Property("dayOfMonth", th.IntegerType),
                    th.Property("firstDay", th.StringType),
                    th.Property("olderThanPeriod", th.StringType),
                    th.Property("olderThanValue", th.IntegerType),
                    th.Property("type", th.StringType),
                ),
            ),
            th.Property("canSeeTimeSheet", th.BooleanType),
            th.Property("canSeeTimeTracker", th.BooleanType),
            th.Property("defaultBillableProjects", th.BooleanType),
            th.Property("forceDescription", th.BooleanType),
            th.Property("forceProjects", th.BooleanType),
            th.Property("forceTags", th.BooleanType),
            th.Property("forceTasks", th.BooleanType),
            th.Property("lockTimeEntries", th.StringType),
            th.Property("onlyAdminsCreateProject", th.BooleanType),
            th.Property("onlyAdminsCreateTag", th.BooleanType),
            th.Property("onlyAdminsSeeAllTimeEntries", th.BooleanType),
            th.Property("onlyAdminsSeeBillableRates", th.BooleanType),
            th.Property("onlyAdminsSeeDashboard", th.BooleanType),
            th.Property("onlyAdminsSeePublicProjectsEntries", th.BooleanType),
            th.Property("projectFavorites", th.BooleanType),
            th.Property("projectGroupingLabel", th.StringType),
            th.Property("projectPickerSpecialFilter", th.BooleanType),
            th.Property(
                "round",
                th.ObjectType(
                    th.Property("minutes", th.StringType),
                    th.Property("round", th.StringType),
                ),
            ),
            th.Property("timeRoundingInReports", th.BooleanType),
            th.Property("trackTimeDownToSecond", th.BooleanType),
        ),
    ),
).to_dict()
