from datetime import datetime

from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserInfo

class ResearchMemberBase(BaseModel):
    role: str = "MEMBER"


class ResearchMemberCreate(BaseModel):
    user_id: int


class ResearchMemberUpdate(BaseModel):
    role: str


class ResearchMemberResponse(ResearchMemberBase):
    project_id: int
    user: UserInfo
    joined_at: datetime

    model_config = ConfigDict(from_attributes=True)