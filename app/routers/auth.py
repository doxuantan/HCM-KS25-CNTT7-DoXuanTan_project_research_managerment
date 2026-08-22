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
