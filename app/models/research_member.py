from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.database import Base
from datetime import datetime


class ResearchMember(Base):
    """
    Bảng lưu thành viên tham gia các đề tài nghiên cứu.
    """

    __tablename__ = "research_members"
    project_id = Column(Integer, ForeignKey("research_projects.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    role = Column(String(20), nullable=False)
    joined_at = Column(DateTime, nullable=False, default=lambda: datetime.now())
    # Quan hệ với ResearchProject
    project = relationship("ResearchProject", back_populates="members")
    # Quan hệ với User
    user = relationship("User", back_populates="memberships")
