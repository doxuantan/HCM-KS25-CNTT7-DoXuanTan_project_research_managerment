from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.db.database import get_db

from app.core.dependencies import (
    get_current_user,
    require_admin,
)

from app.core.responses import success_full
from app.schemas.user import UserResponse

from app.services.user_service import get_users


router = APIRouter(
    prefix="/users",
    tags=["User"],
)


# =========================================================
# DAY 2 - TASK 6
# GET /users/me
# =========================================================
@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
)
def get_me(
    request: Request,
    current_user: User = Depends(get_current_user),
):
    """
    Lấy thông tin người dùng hiện tại.
    """

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Lấy thông tin người dùng thành công",
        data=UserResponse.model_validate(
            current_user
        ).model_dump(),
        request=request,
    )


# =========================================================
# DAY 2 - TASK 7
# GET /users
# =========================================================
@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
def get_users_list(
    request: Request,
    name: str | None = None,
    email: str | None = None,
    is_active: bool | None = None,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """
    Lấy danh sách người dùng.
    Chỉ ADMIN được phép truy cập.
    """

    users = get_users(
        db=db,
        name=name,
        email=email,
        is_active=is_active,
    )

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Lấy danh sách người dùng thành công",
        data=[
            UserResponse.model_validate(
                user
            ).model_dump()
            for user in users
        ],
        request=request,
    )