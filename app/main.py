from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse

from app.db.database import *
from app.models.user import *
from app.models.research_project import *
from app.models.research_member import *
from app.models.research_task import *

from app.routers.auth import router as auth_router
from app.routers.health import router as health_router
from app.routers.user import router as users_router
from app.routers.research_project import router as research_projects_router
from app.routers.research_members import router as research_members_router
from app.core.responses import error_full


app = FastAPI(
    title="Research Group Management API",
    description="Chào mựng bạn đã đến với hệ thống RESEARCH GROUP MANAGEMENT API",
)

Base.metadata.create_all(bind=engine)


# =========================
# EXCEPTION HANDLER
# =========================
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    response = error_full(
        statusCode=exc.status_code,
        message="Request thất bại",
        error=exc.detail,
        request=request,
    )
    return JSONResponse(
        status_code=exc.status_code, content=response.model_dump(mode="json")
    )


# =========================
# ROUTERS
# =========================

app.include_router(auth_router)
app.include_router(health_router)
app.include_router(users_router)
app.include_router(research_projects_router)
app.include_router(research_members_router)


# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {"message": "kết nối tới server thành công"}
