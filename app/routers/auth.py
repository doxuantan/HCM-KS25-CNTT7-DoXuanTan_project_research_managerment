from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.user import *
from app.models.user import *
from app.db.database import *
from app.services.user_service import *
from app.core.security import *
from app.core.responses import success_full


router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.get("/test-db", status_code=status.HTTP_200_OK)
def test_database(request: Request, db: Session = Depends(get_db)):
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


# day 2 -task 3: login


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, request: Request, db: Session = Depends(get_db)):
    """
    Đăng ký tài khoản mới.
    """

    # Kiểm tra email đã tồn tại
    existing_user = db.query(User).filter(User.email == user_data.email).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Email đã được đăng ký"
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

    # Trả response
    return success_full(
        statusCode=status.HTTP_201_CREATED,
        message="Đăng ký tài khoản thành công",
        data=UserResponse.model_validate(new_user).model_dump(),
        request=request,
    )


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    user_data: UserLogin,
    request: Request,
    db: Session = Depends(get_db),
):
    """
    Đăng nhập và nhận access token JWT.
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

    # Trả access token
    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Đăng nhập thành công",
        data={
            "access_token": access_token,
            "token_type": "bearer",
        },
        request=request,
    )
