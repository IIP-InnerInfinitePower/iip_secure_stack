from pydantic import BaseModel, field_validator
class PlanRequest(BaseModel):
    client_id: str
    goal: str = "general"
    @field_validator("client_id")
    @classmethod
    def non_empty(cls, v):
        if not v.strip():
            raise ValueError("client_id required")
        return v
