from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.db.database import get_db

from app.core.dependencies import get_current_user, require_admin
from app.core.responses import success_full

from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["User"])


# day 2-task 6: lấy thông tin người dùng hiện tại
@router.get("/me", status_code=status.HTTP_200_OK)
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
        data=UserResponse.model_validate(current_user).model_dump(),
        request=request,
    )


# day2-task 7
@router.get("", status_code=status.HTTP_200_OK)
def get_users(
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

    query = db.query(User)

    # Tìm theo tên
    if name:
        query = query.filter(User.full_name.ilike(f"%{name}%"))

    # Tìm theo email
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))

    # Lọc theo trạng thái
    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    users = query.all()

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Lấy danh sách người dùng thành công",
        data=[UserResponse.model_validate(user).model_dump() for user in users],
        request=request,
    )
