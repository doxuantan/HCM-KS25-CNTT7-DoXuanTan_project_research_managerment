from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.db.database import Base, engine

from app.models.user import User
from app.models.research_project import ResearchProject
from app.models.research_member import ResearchMember
from app.models.research_task import ResearchTask

from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.user import router as users_router
from app.routers.research_project import router as research_projects_router
from app.routers.research_members import router as research_members_router
from app.routers.research_task import router as research_task_router

from app.core.responses import error_full


app = FastAPI(
    title="Research Group Management API",
    description="Chào mừng bạn đến với hệ thống RESEARCH GROUP MANAGEMENT API",
)


# =========================
# CREATE DATABASE TABLES
# =========================
Base.metadata.create_all(bind=engine)


# =========================
# HTTP EXCEPTION HANDLER
# =========================
@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    response = error_full(
        statusCode=exc.status_code,
        message="Request thất bại",
        error=exc.detail,
        request=request,
    )

    return JSONResponse(
        status_code=exc.status_code,
        content=response.model_dump(mode="json"),
    )


# =========================
# VALIDATION EXCEPTION HANDLER
# =========================
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    response = error_full(
        statusCode=422,
        message="Dữ liệu không hợp lệ",
        error=exc.errors(),
        request=request,
    )

    return JSONResponse(
        status_code=422,
        content=response.model_dump(mode="json"),
    )


# =========================
# ROUTERS
# =========================
app.include_router(auth_router)
app.include_router(health_router)
app.include_router(users_router)
app.include_router(research_projects_router)
app.include_router(research_members_router)
app.include_router(research_task_router)


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "message": "kết nối tới server thành công"
    }