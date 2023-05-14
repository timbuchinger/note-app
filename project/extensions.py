import os

import pymongo

uri = os.getenv(
    "MONGO_URI",
    default="mongodb://admin:password@localhost:27017/?authMechanism=DEFAULT",
)

mongo = pymongo.MongoClient(
    host=uri,
    serverSelectionTimeoutMS=1000,
).get_database("assessment")

mongo["notes"].create_index(
    [
        ("content", "text"),
        (
            "title",
            "text",
        ),
    ]
)
