from fastapi import APIRouter, Depends, Request, status

from app.models.user import User
from app.core.dependencies import get_current_user
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
