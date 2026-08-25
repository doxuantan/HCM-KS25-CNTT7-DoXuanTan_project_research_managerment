from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.models.user import User
from app.db.database import get_db

from app.core.responses import success_full
from app.core.dependencies import require_admin

from app.services.auth_service import (
    register_user,
    login_user,
)


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"],
)


# =========================================================
# TEST DATABASE
# =========================================================
@router.get(
    "/test-db",
    status_code=status.HTTP_200_OK,
)
def test_database(
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Kiểm tra kết nối Database.
    """

    db.execute(text("SELECT 1"))

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Kết nối database thành công",
        data={"database": "Connected"},
        request=request,
    )


# =========================================================
# REGISTER
# =========================================================
@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Đăng ký tài khoản mới.
    """

    new_user = register_user(
        user_data=user_data,
        db=db,
    )

    return success_full(
        statusCode=status.HTTP_201_CREATED,
        message="Đăng ký tài khoản thành công",
        data=UserResponse.model_validate(new_user).model_dump(),
        request=request,
    )


# =========================================================
# LOGIN
# =========================================================
@router.post(
    "/login",
    status_code=status.HTTP_200_OK,
)
def login(
    user_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Đăng nhập và nhận access token JWT.
    """

    token_data = login_user(
        user_data=user_data,
        db=db,
    )

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Đăng nhập thành công",
        data=token_data,
        request=request,
    )


# =========================================================
# HELLO ADMIN
# =========================================================
@router.get(
    "/hello",
    status_code=status.HTTP_200_OK,
)
def hello_admin(
    request: Request,
    current_user: User = Depends(require_admin),
):
    """
    Xin chào ADMIN.
    Chỉ ADMIN mới được truy cập.
    """

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Xin chào Admin",
        data={
            "message": f"Xin chào Admin {current_user.full_name}",
        },
        request=request,
    )
