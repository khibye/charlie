from datetime import datetime

from pydantic import BaseModel, Field


class SummarizeRequest(BaseModel):
    country: str = Field(..., description="Country name")
    city: str = Field(..., description="City name")
    user_id: str = Field(..., description="User id")
    date_from: datetime | None = Field(None, description="ISO datetime")
    date_to: datetime | None = Field(None, description="ISO datetime")
    prompt: str | None = Field(
        None,
        description="Optional prompt override for the summarize generator",
    )
