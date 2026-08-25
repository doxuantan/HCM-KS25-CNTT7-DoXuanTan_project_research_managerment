from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
import jwt

from app.core.config import settings
from app.db.database import get_db
from app.models.user import User


security = HTTPBearer()
# day 2-task 4
# Nhận JWT mà client gửi lên → kiểm tra JWT có hợp lệ không → tìm User tương ứng trong database → trả về User đó.
# Nó chính là cầu nối giữa JWT và User trong database.


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    # Lấy access token từ Authorization: Bearer <token>
    token = credentials.credentials
    try:
        # Giải mã và kiểm tra JWT
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )
        # Lấy user_id từ claim sub
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không hợp lệ",
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token đã hết hạn",
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ",
        )

    # Tìm user trong database
    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Người dùng không tồn tại",
        )

    # Kiểm tra tài khoản còn hoạt động
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tài khoản đã bị khóa",
        )

    return user


# day 2- task 5: Role guard


def require_admin(current_user: User = Depends(get_current_user)):
    # Chỉ cho phép ADMIN
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Bạn không có quyền truy cập"
        )

    return current_user
