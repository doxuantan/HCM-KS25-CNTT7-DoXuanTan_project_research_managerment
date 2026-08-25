from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ResearchTaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
    )

    description: Optional[str] = None

    assignee_id: Optional[int] = None

    status: str = "TODO"

    priority: str = "MEDIUM"

    due_date: Optional[datetime] = None


class ResearchTaskCreate(ResearchTaskBase):
    pass


class ResearchTaskUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
    )

    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[datetime] = None


class ResearchTaskResponse(ResearchTaskBase):
    id: int
    project_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)