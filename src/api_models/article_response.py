from typing import Any

from pydantic import BaseModel, Field


class ArticleResponse(BaseModel):
    article: str
    meta: dict[str, Any] = Field(default_factory=dict)
