from fastapi import APIRouter, Depends, status, Request
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
