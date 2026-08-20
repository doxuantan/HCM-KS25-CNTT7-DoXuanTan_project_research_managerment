from fastapi import APIRouter, Request, status

from app.core.responses import success_full


router = APIRouter(prefix="/api/health", tags=["Health"])


@router.get("")
def health_check(request: Request):

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="API đang hoạt động",
        data={"status": "healthy"},
        request=request,
    )
