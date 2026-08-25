from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User

from app.schemas.research_member import (
    ResearchMemberCreate,
    ResearchMemberResponse,
)

from app.core.dependencies import get_current_user
from app.core.responses import success_full

from app.services.research_member_service import (
    add_member,
    get_members,
    delete_member,
)


router = APIRouter(
    prefix="/research-projects",
    tags=["Research Member"],
)


# =========================================================
# POST /research-projects/{project_id}/members
# Thêm thành viên
# =========================================================
@router.post(
    "/{project_id}/members",
    status_code=status.HTTP_201_CREATED,
)
def add_project_member(
    project_id: int,
    member_data: ResearchMemberCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    OWNER thêm user vào đề tài nghiên cứu.
    """

    member = add_member(
        db=db,
        project_id=project_id,
        user_id=member_data.user_id,
        current_user_id=current_user.id,
    )

    return success_full(
        statusCode=status.HTTP_201_CREATED,
        message="Thêm thành viên thành công",
        data=ResearchMemberResponse.model_validate(
            member
        ).model_dump(),
        request=request,
    )


# =========================================================
# GET /research-projects/{project_id}/members
# Danh sách thành viên
# =========================================================
@router.get(
    "/{project_id}/members",
    status_code=status.HTTP_200_OK,
)
def get_project_members(
    project_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    OWNER hoặc MEMBER được xem danh sách thành viên.
    """

    members = get_members(
        db=db,
        project_id=project_id,
        current_user_id=current_user.id,
    )

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Lấy danh sách thành viên thành công",
        data=[
            ResearchMemberResponse.model_validate(
                member
            ).model_dump()
            for member in members
        ],
        request=request,
    )


# =========================================================
# DELETE /research-projects/{project_id}/members/{user_id}
# Xóa thành viên
# =========================================================
@router.delete(
    "/{project_id}/members/{user_id}",
    status_code=status.HTTP_200_OK,
)
def delete_project_member(
    project_id: int,
    user_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    OWNER xóa thành viên.
    Không được xóa OWNER.
    """

    delete_member(
        db=db,
        project_id=project_id,
        user_id=user_id,
        current_user_id=current_user.id,
    )

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Xóa thành viên thành công",
        data=None,
        request=request,
    )