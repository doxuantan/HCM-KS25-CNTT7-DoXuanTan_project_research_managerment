from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.research_project import ResearchProject
from app.models.user import User
from app.models.research_member import ResearchMember
from app.models.research_task import ResearchTask
from app.schemas.research_project import (
    ResearchProjectCreate,
    ResearchProjectUpdate,
)


from app.core.exceptions import *

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

    # Kiểm tra tên đề tài
    if not project_data.name.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên đề tài không được để trống",
        )

    # Kiểm tra user tồn tại
    user = (
        db.query(User)
        .filter(User.id == owner_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại",
        )

    # Tạo project
    new_project = ResearchProject(
        name=project_data.name.strip(),
        description=project_data.description,
        owner_id=owner_id,
    )

    db.add(new_project)

    # Lưu project để lấy new_project.id
    db.commit()
    db.refresh(new_project)

    # Tạo member với role OWNER
    owner_member = ResearchMember(
        project_id=new_project.id,
        user_id=owner_id,
        role="OWNER",
    )

    db.add(owner_member)
    db.commit()

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

    Có thể tìm kiếm theo tên project.
    """

    # Lấy project mà user là OWNER
    owner_projects = (
        db.query(ResearchProject)
        .filter(
            ResearchProject.owner_id == user_id
        )
        .all()
    )

    # Lấy các project mà user là MEMBER
    member_records = (
        db.query(ResearchMember)
        .filter(
            ResearchMember.user_id == user_id
        )
        .all()
    )

    # Bắt đầu với danh sách OWNER
    projects = owner_projects.copy()

    # Thêm project mà user là MEMBER
    for member in member_records:
        project = (
            db.query(ResearchProject)
            .filter(
                ResearchProject.id == member.project_id
            )
            .first()
        )

        if project and project not in projects:
            projects.append(project)

    # Search theo tên
    if name:
        name = name.strip()

        if name:
            projects = [
                project
                for project in projects
                if name.lower() in project.name.lower()
            ]
        else:
            projects = []

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
    Lấy chi tiết đề tài nghiên cứu.
    Chỉ OWNER hoặc MEMBER mới được xem.
    """

    # Tìm project
    project = (
        db.query(ResearchProject)
        .filter(
            ResearchProject.id == project_id
        )
        .first()
    )

    # Project không tồn tại
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đề tài nghiên cứu không tồn tại",
        )

    # OWNER được xem
    if project.owner_id == user_id:
        return project

    # Kiểm tra user có phải MEMBER không
    member = (
        db.query(ResearchMember)
        .filter(
            ResearchMember.project_id == project_id,
            ResearchMember.user_id == user_id,
        )
        .first()
    )

    # Không phải OWNER và cũng không phải MEMBER
    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của đề tài nghiên cứu",
        )

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
    project = (
        db.query(ResearchProject)
        .filter(
            ResearchProject.id == project_id
        )
        .first()
    )

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

        # Không cho tên rỗng / toàn khoảng trắng
        if not project_data.name.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tên đề tài không được để trống",
            )

        # Lưu tên đã loại bỏ khoảng trắng đầu/cuối
        project.name = project_data.name.strip()

    # Cập nhật description
    if project_data.description is not None:
        project.description = project_data.description

    # Lưu database
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
    project = (
        db.query(ResearchProject)
        .filter(
            ResearchProject.id == project_id
        )
        .first()
    )

    if project is None:
        raise not_found("Đề tài nghiên cứu không tồn tại")

    # Kiểm tra OWNER
    if project.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới được xóa đề tài nghiên cứu",
        )

    # Xóa các task thuộc project
    db.query(ResearchTask).filter(
        ResearchTask.project_id == project_id
    ).delete(
        synchronize_session=False
    )

    # Xóa các member thuộc project
    db.query(ResearchMember).filter(
        ResearchMember.project_id == project_id
    ).delete(
        synchronize_session=False
    )

    # Xóa project
    db.delete(project)
    db.commit()

    return True