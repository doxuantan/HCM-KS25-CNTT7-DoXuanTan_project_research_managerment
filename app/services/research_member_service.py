from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.research_member import ResearchMember
from app.models.research_project import ResearchProject
from app.models.user import User


# =========================================================
# THÊM THÀNH VIÊN
# =========================================================
def add_member(
    db: Session,
    project_id: int,
    user_id: int,
    current_user_id: int,
):
    """
    Owner thêm user vào project.
    Không cho thêm trùng.
    """

    # Tìm project
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đề tài nghiên cứu không tồn tại",
        )

    # Kiểm tra OWNER
    if project.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới được thêm thành viên",
        )

    # Kiểm tra user tồn tại
    user = db.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Người dùng không tồn tại",
        )

    # Kiểm tra đã là member chưa
    existing_member = (
        db.query(ResearchMember)
        .filter(
            ResearchMember.project_id == project_id,
            ResearchMember.user_id == user_id,
        )
        .first()
    )

    if existing_member:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Người dùng đã là thành viên",
        )

    # Tạo member
    new_member = ResearchMember(
        project_id=project_id,
        user_id=user_id,
        role="MEMBER",
    )

    db.add(new_member)
    db.commit()
    db.refresh(new_member)

    return new_member


# =========================================================
# DANH SÁCH THÀNH VIÊN
# =========================================================
def get_members(
    db: Session,
    project_id: int,
    current_user_id: int,
):
    """
    Lấy danh sách thành viên.
    OWNER hoặc MEMBER được xem.
    """

    # Tìm project
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đề tài nghiên cứu không tồn tại",
        )

    # Kiểm tra user là OWNER
    if project.owner_id == current_user_id:
        return (
            db.query(ResearchMember)
            .filter(ResearchMember.project_id == project_id)
            .all()
        )

    # Kiểm tra user là MEMBER
    member = (
        db.query(ResearchMember)
        .filter(
            ResearchMember.project_id == project_id,
            ResearchMember.user_id == current_user_id,
        )
        .first()
    )

    if member is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không phải thành viên của đề tài",
        )

    return (
        db.query(ResearchMember).filter(ResearchMember.project_id == project_id).all()
    )


# =========================================================
# XÓA THÀNH VIÊN
# =========================================================
def delete_member(
    db: Session,
    project_id: int,
    user_id: int,
    current_user_id: int,
):
    """
    Owner xóa member.
    Không được xóa OWNER.
    """

    # Tìm project
    project = db.query(ResearchProject).filter(ResearchProject.id == project_id).first()

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đề tài nghiên cứu không tồn tại",
        )

    # Kiểm tra OWNER
    if project.owner_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới được xóa thành viên",
        )

    # Tìm member
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
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Thành viên không tồn tại",
        )

    # Không cho xóa OWNER
    if member.role == "OWNER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Không được xóa OWNER",
        )

    db.delete(member)
    db.commit()
