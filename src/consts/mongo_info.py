from enum import StrEnum


class MongoInfo(StrEnum):
    URI = "mongodb://localhost:27017"
    DB_NAME = "local"
    RAW_DATA_COLLECTION = "special_data"
    CONTEXT_COLLECTION = "contexts"
