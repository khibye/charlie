from typing import Any

from pydantic import BaseModel, Field


class ContextResponse(BaseModel):
    context: str
    meta: dict[str, Any] = Field(default_factory=dict)
