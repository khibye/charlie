from typing import Any

from pydantic import BaseModel, Field


class SummarizeResponse(BaseModel):
    summarize: str
    meta: dict[str, Any] = Field(default_factory=dict)
