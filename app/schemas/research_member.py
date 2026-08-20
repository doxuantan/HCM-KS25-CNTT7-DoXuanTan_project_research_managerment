from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResearchMemberBase(BaseModel):
    role: str = "MEMBER"


class ResearchMemberCreate(ResearchMemberBase):
    project_id: int
    user_id: int


class ResearchMemberUpdate(BaseModel):
    role: str


class ResearchMemberResponse(ResearchMemberBase):
    project_id: int
    user_id: int
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)
