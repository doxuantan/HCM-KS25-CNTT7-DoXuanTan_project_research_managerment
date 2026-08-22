from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base
from datetime import datetime


class ResearchTask(Base):
    """
    Bảng lưu các nhiệm vụ nghiên cứu.
    """

    __tablename__ = "research_tasks"
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("research_projects.id"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    assignee_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String(30), nullable=False)
    priority = Column(String(20), nullable=False)
    due_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=lambda: datetime.now())

    # Task thuộc về một ResearchProject
    project = relationship("ResearchProject", back_populates="tasks")

    # User được giao task
    assignee = relationship("User", back_populates="assigned_tasks")
