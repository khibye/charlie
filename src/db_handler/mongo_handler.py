from datetime import datetime
from typing import Any

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorCursor, AsyncIOMotorDatabase

from consts.defaults import DEFAULT_CONTEXT
from consts.mongo_info import MongoInfo
from db_handler.db_handler import DBHandler


class MongoHandler(DBHandler):
    """Handles interactions with MongoDB."""

    def __init__(self, mongo_db: AsyncIOMotorDatabase) -> None:
        self.mongo_db: AsyncIOMotorDatabase = mongo_db
        self.raw_data_collection: AsyncIOMotorCollection = self.mongo_db[
            MongoInfo.RAW_DATA_COLLECTION
        ]
        self.context_collection: AsyncIOMotorCollection = self.mongo_db[
            MongoInfo.CONTEXT_COLLECTION
        ]

    async def fetch_raw_data(
        self,
        country: str,
        city: str,
        date_from: datetime,
        date_to: datetime,
    ) -> list[str]:
        """Fetch all raw documents relevant to (country, city) within an optional date range in MongoDB."""

        filter_query: dict[str, Any] = {
            "country": country,
            "city": city,
            # TODO: Add date
        }
        projection_query: dict[str, bool] = {
            "_id": False,
            "data": True,
        }

        documents: AsyncIOMotorCursor = await self.raw_data_collection.find(
            filter=filter_query,
            projection=projection_query,
        ).to_list()

        return [doc["data"] for doc in documents]

    async def fetch_user_context(
        self,
        country: str,
        city: str,
        user_id: str,
    ) -> str:
        """Fetch user_context unique per (country, city, user_id) in MongoDB."""

        filter_query: dict[str, Any] = {
            "country": country,
            "city": city,
            "user_id": user_id,
        }
        projection_query: dict[str, bool] = {
            "_id": False,
            "context": True,
        }

        await self.context_collection.update_one(
            filter=filter_query,
            update={"$setOnInsert": {"context": DEFAULT_CONTEXT}},
            upsert=True,
        )

        return (
            await self.context_collection.find_one(
                filter=filter_query,
                projection=projection_query,
            )
            or {}
        ).get("context", DEFAULT_CONTEXT)
