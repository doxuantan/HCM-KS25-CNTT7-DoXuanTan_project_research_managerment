from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ResearchTaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    assignee_id: Optional[int] = None
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: Optional[datetime] = None


class ResearchTaskCreate(ResearchTaskBase):
    project_id: int


class ResearchTaskUpdate(BaseModel):
    title: Optional[str] = None
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
