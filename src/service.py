from datetime import datetime, timedelta

import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
)

from api_models import ArticleResponse
from consts.mongo_info import MongoInfo
from db_handler.mongo_handler import MongoHandler
from llm import ArticleLLMCreator, ContextImprover
from llm.clients import BaseLLMClient, GLM5SelfHostedClient, QwenLocalCPUClient


class Service:
    def __init__(self) -> None:
        self.app = FastAPI(title="Article Creator Service")
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=[
                "http://localhost:5173",
                "http://127.0.0.1:5173",
            ],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Mongo
        self.mongo: AsyncIOMotorClient = AsyncIOMotorClient(MongoInfo.URI)
        self.db: AsyncIOMotorDatabase = self.mongo[MongoInfo.DB_NAME]
        self.mongo_handler = MongoHandler(self.db)

        # LLM pipeline components
        self.llm: BaseLLMClient = GLM5SelfHostedClient()
        self.article_creator = ArticleLLMCreator(self.llm)
        self.context_improver = ContextImprover(self.llm)

        # Routes
        self.app.add_api_route(
            "/article",
            self.get_article,
            methods=["GET"],
            response_model=ArticleResponse,
        )

    async def get_article(
        self,
        country: str = Query(...),
        city: str = Query(...),
        user_id: str = Query(default="default_user"),
        date_from: str = Query(default=""),
        date_to: str = Query(default=""),
    ) -> ArticleResponse:
        """Main endpoint: fetch data + context and run the article creation pipeline."""

        date_to = datetime.fromisoformat(date_to if date_to else datetime.now().isoformat())
        date_from = datetime.fromisoformat(
            date_from if date_from else (date_to - timedelta(days=60)).isoformat()
        )

        fetched_data: list[str] = await self.mongo_handler.fetch_raw_data(
            country=country,
            city=city,
            date_from=date_from,
            date_to=date_to,
        )

        user_context: str = await self.mongo_handler.fetch_user_context(
            country=country,
            city=city,
            user_id=user_id,
        )

        article: str = await self.article_creator.create_article(
            fetched_data=fetched_data,
            user_context=user_context,
        )

        logger.info("Done creating article", country=country, city=city, user_id=user_id)

        return ArticleResponse(
            article=article,
            meta={
                "country": country,
                "city": city,
                "user_id": user_id,
                "count": len(fetched_data),
                "context": user_context,
            },
        )


service = Service()


if __name__ == "__main__":
    uvicorn.run(service.app, host="0.0.0.0", port=8000)
