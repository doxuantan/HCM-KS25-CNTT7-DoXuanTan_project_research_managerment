from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ResearchProjectBase(BaseModel):
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )
    description: Optional[str] = None


class ResearchProjectCreate(ResearchProjectBase):
    pass


class ResearchProjectUpdate(BaseModel):
    name: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description: Optional[str] = None


class ResearchProjectResponse(ResearchProjectBase):
    id: int
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)