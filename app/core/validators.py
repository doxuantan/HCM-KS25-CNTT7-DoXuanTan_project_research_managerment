from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.research_project import ResearchProject
from app.models.research_member import ResearchMember


# =========================================================
# Kiểm tra project và user có thuộc project không
# =========================================================
def check_project_member(
    db: Session,
    project_id: int,
    user_id: int,
):
    """
    Kiểm tra:
    - Project có tồn tại không
    - User có phải OWNER hoặc MEMBER của project không
    """
    # Tìm project
    project = (
        db.query(ResearchProject)
        .filter(ResearchProject.id == project_id)
        .first()
    )
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đề tài nghiên cứu không tồn tại",
        )
    # User là OWNER
    if project.owner_id == user_id:
        return project

    # User là MEMBER
    member = (
        db.query(ResearchMember)
        .filter(
            ResearchMember.project_id == project_id,
            ResearchMember.user_id == user_id,
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của đề tài nghiên cứu",
        )
    return project


# =========================================================
# Kiểm tra user được giao task có thuộc project không
# =========================================================
def check_user_in_project(
    db: Session,
    project_id: int,
    user_id: int,
):
    """
    Kiểm tra user có thuộc project không.
    OWNER và MEMBER đều được tính là thành viên project.
    """

    # Tìm project
    project = (
        db.query(ResearchProject)
        .filter(ResearchProject.id == project_id)
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đề tài nghiên cứu không tồn tại",
        )

    # OWNER
    if project.owner_id == user_id:
        return True

    # MEMBER
    member = (
        db.query(ResearchMember)
        .filter(
            ResearchMember.project_id == project_id,
            ResearchMember.user_id == user_id,
        )
        .first()
    )

    if member is None:
        return False
    return True


# =========================================================
# Kiểm tra status
# =========================================================
def validate_status(task_status: str):
    """
    Status hợp lệ:
    TODO
    IN_PROGRESS
    DONE
    """

    allowed_status = [
        "TODO",
        "IN_PROGRESS",
        "DONE",
    ]

    if task_status not in allowed_status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status không hợp lệ",
        )


# =========================================================
# Kiểm tra priority
# =========================================================
def validate_priority(priority: str):
    """
    Priority hợp lệ:
    LOW
    MEDIUM
    HIGH
    """

    allowed_priority = [
        "LOW",
        "MEDIUM",
        "HIGH",
    ]

    if priority not in allowed_priority:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Priority không hợp lệ",
        )