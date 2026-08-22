from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResearchProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ResearchProjectCreate(ResearchProjectBase):
    owner_id: int


class ResearchProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None


class ResearchProjectResponse(ResearchProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
