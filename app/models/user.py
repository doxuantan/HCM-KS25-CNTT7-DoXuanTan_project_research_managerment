from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    """
    Bảng lưu thông tin người dùng.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False, default="USER")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False)
    # User sở hữu nhiều ResearchProject
    projects = relationship("ResearchProject", back_populates="owner")
    # User tham gia nhiều ResearchProject
    memberships = relationship("ResearchMember", back_populates="user")
    # User có thể được giao nhiều ResearchTask
    assigned_tasks = relationship("ResearchTask", back_populates="assignee")
