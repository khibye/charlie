from pydantic import BaseModel, Field


class ManualImproveContextRequest(BaseModel):
    country: str = Field(..., description="Country name")
    city: str = Field(..., description="City name")
    user_id: str = Field(..., description="User id")
    new_context: str = Field(..., description="Full replacement context text")
