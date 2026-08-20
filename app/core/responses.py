from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime, timezone
from fastapi import Request


class APIResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any]
    error: Optional[Any]
    datetime: str
    path: str


def success_full(statusCode: int, message: str, data: Any, request: Request):
    return APIResponse(
        statusCode=statusCode,
        message=message,
        data=data,
        error=None,
        datetime=datetime.now(timezone.utc).isoformat(),
        path=request.url.path,
    )


def error_full(statusCode: int, message: str, error: Any, request: Request):
    return APIResponse(
        statusCode=statusCode,
        message=message,
        data=None,
        error=error,
        datetime=datetime.now(timezone.utc).isoformat(),
        path=request.url.path,
    )
