from pydantic import BaseModel, Field


class LLMImproveContextRequest(BaseModel):
    country: str = Field(..., description="Country name")
    city: str = Field(..., description="City name")
    user_id: str = Field(..., description="User id")
    context_request_clarification: str = Field(
        ...,
        description="Natural language clarification used to improve existing context",
    )
