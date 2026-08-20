from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base


class ResearchProject(Base):
    """
    Bảng lưu thông tin các đề tài nghiên cứu.
    """
    __tablename__ = "research_projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, nullable=False)
    # Người sở hữu project
    owner = relationship("User", back_populates="projects")
    # Danh sách thành viên của project
    members = relationship("ResearchMember", back_populates="project")
    # Danh sách task của project
    tasks = relationship("ResearchTask", back_populates="project")
