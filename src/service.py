from datetime import datetime, timedelta

import uvicorn
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from loguru import logger
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorDatabase,
)

from api_models import (
    ContextResponse,
    LLMImproveContextRequest,
    ManualImproveContextRequest,
    SummarizeResponse,
)
from consts import MongoInfo
from db_handler.mongo_handler import MongoHandler
from llm import LLMContextImprover, LLMSummarizeCreator
from llm.clients import BaseLLMClient, GLM5SelfHostedClient, QwenLocalCPUClient


class Service:
    def __init__(self) -> None:
        self.app = FastAPI(title="Summarize Creator Service")
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
        self.summarize_creator = LLMSummarizeCreator(self.llm)
        self.llm_context_improver = LLMContextImprover(self.llm)

        # Routes
        self.app.add_api_route(
            "/summarize",
            self.get_summarize,
            methods=["GET"],
            response_model=SummarizeResponse,
        )
        self.app.add_api_route(
            "/summarize-stream",
            self.get_summarize_stream,
            methods=["GET"],
        )
        self.app.add_api_route(
            "/context",
            self.get_context,
            methods=["GET"],
            response_model=ContextResponse,
        )
        self.app.add_api_route(
            "/llm-improve-context",
            self.llm_improve_context,
            methods=["POST"],
        )
        self.app.add_api_route(
            "/manual-improve-context",
            self.manual_improve_context,
            methods=["POST"],
        )

    async def get_summarize(
        self,
        country: str = Query(...),
        city: str = Query(...),
        user_id: str = Query(...),
        date_from: str = Query(default=""),
        date_to: str = Query(default=""),
    ) -> SummarizeResponse:
        """Main endpoint: fetch data + context and run the summarize creation pipeline."""

        date_to: datetime = datetime.fromisoformat(
            date_to if date_to else datetime.now().isoformat()
        )
        date_from: datetime = datetime.fromisoformat(
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

        summarize: str = await self.summarize_creator.create_summarize(
            fetched_data=fetched_data,
            user_context=user_context,
        )

        logger.info("Done creating summarize", country=country, city=city, user_id=user_id)

        return SummarizeResponse(
            summarize=summarize,
            meta={
                "country": country,
                "city": city,
                "user_id": user_id,
                "count": len(fetched_data),
                "context": user_context,
            },
        )

    async def get_context(
        self,
        country: str = Query(...),
        city: str = Query(...),
        user_id: str = Query(...),
    ) -> ContextResponse:
        context = await self.mongo_handler.fetch_user_context(
            country=country,
            city=city,
            user_id=user_id,
        )
        return ContextResponse(
            context=context,
            meta={
                "country": country,
                "city": city,
                "user_id": user_id,
            },
        )

    async def get_summarize_stream(
        self,
        country: str = Query(...),
        city: str = Query(...),
        user_id: str = Query(...),
        date_from: str = Query(default=""),
        date_to: str = Query(default=""),
    ) -> StreamingResponse:

        date_to: datetime = datetime.fromisoformat(
            date_to if date_to else datetime.now().isoformat()
        )
        date_from: datetime = datetime.fromisoformat(
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

        logger.info("Starting summarize stream", country=country, city=city, user_id=user_id)

        stream = self.summarize_creator.create_summarize_stream(
            fetched_data=fetched_data,
            user_context=user_context,
        )

        return StreamingResponse(
            stream,
            media_type="text/plain; charset=utf-8",
            headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
        )

    async def manual_improve_context(
        self,
        request: ManualImproveContextRequest,
    ) -> None:
        await self.mongo_handler.update_user_context(
            country=request.country,
            city=request.city,
            user_id=request.user_id,
            new_context=request.new_context,
        )

    async def llm_improve_context(
        self,
        request: LLMImproveContextRequest,
    ) -> None:
        current_context: str = await self.mongo_handler.fetch_user_context(
            country=request.country,
            city=request.city,
            user_id=request.user_id,
        )

        improved_context: str = await self.llm_context_improver.improve_with_llm(
            current_context=current_context,
            context_request_clarification=request.context_request_clarification,
        )

        await self.mongo_handler.update_user_context(
            country=request.country,
            city=request.city,
            user_id=request.user_id,
            new_context=improved_context,
        )


service = Service()


if __name__ == "__main__":
    uvicorn.run(service.app, host="0.0.0.0", port=8000)
