import bcrypt
import jwt

from datetime import datetime, timedelta, timezone

from app.core.config import settings


# task 2 ngày 2
def hash_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode("utf-8")


# task 3 ngày 2 login
def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


# tạo accsess token
def create_access_token(user_id: int, role: str) -> str:
    expire_time = datetime.now(timezone.utc) + timedelta(
        minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # tấm vé
    payload = {"sub": str(user_id), "role": role, "exp": expire_time}

    access_token = jwt.encode(
        payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return access_token
