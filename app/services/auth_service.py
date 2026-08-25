from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserLogin
from app.models.user import User

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)


# =========================================================
# REGISTER
# =========================================================
def register_user(
    user_data: UserCreate,
    db: Session,
):
    """
    Xử lý đăng ký tài khoản mới.
    """

    # Kiểm tra email đã tồn tại
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email đã được đăng ký",
        )

    # Hash mật khẩu
    password_hash = hash_password(user_data.password)

    # Tạo user mới
    new_user = User(
        email=user_data.email,
        full_name=user_data.full_name,
        password_hash=password_hash,
    )

    # Lưu vào database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# =========================================================
# LOGIN
# =========================================================
def login_user(
    user_data: UserLogin,
    db: Session,
):
    """
    Xử lý đăng nhập và tạo access token JWT.
    """

    # Tìm user theo email
    user = db.query(User).filter(User.email == user_data.email).first()

    # Email không tồn tại
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
        )

    # Kiểm tra mật khẩu
    if not verify_password(
        user_data.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không chính xác",
        )

    # Kiểm tra tài khoản có đang hoạt động không
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị khóa",
        )

    # Tạo access token JWT
    access_token = create_access_token(
        user_id=user.id,
        role=user.role,
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
