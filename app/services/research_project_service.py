from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.research_project import ResearchProject
from app.models.research_member import ResearchMember
from app.schemas.research_project import (
    ResearchProjectCreate,
    ResearchProjectUpdate,
)


# =========================================================
# TASK 1: Tạo đề tài nghiên cứu
# =========================================================
def create_research_project(
    db: Session,
    project_data: ResearchProjectCreate,
    owner_id: int,
):
    """
    Tạo đề tài nghiên cứu.
    User đăng nhập sẽ trở thành OWNER.
    """

    new_project = ResearchProject(
        name=project_data.name,
        description=project_data.description,
        owner_id=owner_id,
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


# =========================================================
# TASK 2: Lấy danh sách đề tài nghiên cứu
# =========================================================
def get_research_projects(
    db: Session,
    user_id: int,
    name: str | None = None,
):
    """
    Lấy danh sách project mà user là OWNER hoặc MEMBER.
    """

    owner_projects = (
        db.query(ResearchProject).filter(ResearchProject.owner_id == user_id).all()
    )
    member_records = (
        db.query(ResearchMember).filter(ResearchMember.user_id == user_id).all()
    )

    projects = owner_projects.copy()

    for member in member_records:
        project = (
            db.query(ResearchProject)
            .filter(ResearchProject.id == member.project_id)
            .first()
        )

        if project and project not in projects:
            projects.append(project)

    if name:
        projects = [
            project for project in projects if name.lower() in project.name.lower()
        ]

    return projects


# =========================================================
# TASK 3: Chi tiết đề tài nghiên cứu
# =========================================================
def get_research_project_detail(
    db: Session,
    project_id: int,
    user_id: int,
):
    """
    Lấy chi tiết project.
    Chỉ OWNER hoặc MEMBER mới được xem.
    """

    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đề tài nghiên cứu không tồn tại",
        )
    
    if project.owner_id == user_id:
        return project

    # member = (
    #     db.query(ResearchMember)
    #     .filter(
    #         ResearchMember.project_id == project_id,
    #         ResearchMember.user_id == user_id,
    #     )
    #     .first()
    # )
    
    if project.members is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Bạn không phải thành viên của đề tài nghiên cứu",
            )

    # if member is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_403_FORBIDDEN,
    #         detail="Bạn không phải thành viên của đề tài nghiên cứu",
    #     )

    return project


# =========================================================
# TASK 4: Cập nhật đề tài nghiên cứu
# =========================================================
def update_research_project(
    db: Session,
    project_id: int,
    user_id: int,
    project_data: ResearchProjectUpdate,
):
    """
    Cập nhật đề tài nghiên cứu.
    Chỉ OWNER mới được cập nhật.
    """

    # Tìm project
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đề tài nghiên cứu không tồn tại",
        )

    # Kiểm tra OWNER
    if project.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới được cập nhật đề tài nghiên cứu",
        )

    # Cập nhật name
    if project_data.name is not None:
        project.name = project_data.name

    # Cập nhật description
    if project_data.description is not None:
        project.description = project_data.description

    db.commit()
    db.refresh(project)

    return project


# =========================================================
# TASK 4: Xóa đề tài nghiên cứu
# =========================================================
def delete_research_project(
    db: Session,
    project_id: int,
    user_id: int,
):
    """
    Xóa đề tài nghiên cứu.
    Chỉ OWNER mới được xóa.
    """

    # Tìm project
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đề tài nghiên cứu không tồn tại",
        )

    # Kiểm tra OWNER
    if project.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới được xóa đề tài nghiên cứu",
        )

    db.delete(project)
    db.commit()

    return True
