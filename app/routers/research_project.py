from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User

from app.schemas.research_project import (
    ResearchProjectCreate,
    ResearchProjectUpdate,
    ResearchProjectResponse,
)

from app.core.dependencies import get_current_user
from app.core.responses import success_full

from app.services.research_project_service import (
    create_research_project,
    get_research_projects,
    get_research_project_detail,
    update_research_project,
    delete_research_project,
)


router = APIRouter(
    prefix="/research-projects",
    tags=["Research Project"],
)


# =========================================================
# TASK 1
# POST /research-projects
# =========================================================
@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project_data: ResearchProjectCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Tạo đề tài nghiên cứu.
    User đăng nhập sẽ trở thành OWNER.
    """

    new_project = create_research_project(
        db=db,
        project_data=project_data,
        owner_id=current_user.id,
    )

    return success_full(
        statusCode=status.HTTP_201_CREATED,
        message="Tạo đề tài nghiên cứu thành công",
        data=ResearchProjectResponse.model_validate(new_project).model_dump(),
        request=request,
    )


# =========================================================
# TASK 2
# GET /research-projects
# =========================================================
@router.get(
    "",
    status_code=status.HTTP_200_OK,
)
def get_project_list(
    request: Request,
    name: str | None = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Lấy danh sách đề tài nghiên cứu.

    Chỉ trả về project mà user:
    - là OWNER
    - hoặc là MEMBER

    Có thể tìm kiếm theo tên đề tài.
    """

    projects = get_research_projects(
        db=db,
        user_id=current_user.id,
        name=name,
    )

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Lấy danh sách đề tài nghiên cứu thành công",
        data=[
            ResearchProjectResponse.model_validate(project).model_dump()
            for project in projects
        ],
        request=request,
    )


# =========================================================
# TASK 3
# GET /research-projects/{project_id}
# =========================================================
@router.get(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
)
def get_project_detail(
    project_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Lấy chi tiết đề tài nghiên cứu.

    Chỉ OWNER hoặc MEMBER mới được xem.
    """

    project = get_research_project_detail(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
    )

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Lấy chi tiết đề tài nghiên cứu thành công",
        data=ResearchProjectResponse.model_validate(project).model_dump(),
        request=request,
    )


# =========================================================
# TASK 4
# PATCH /research-projects/{project_id}
# =========================================================
@router.patch(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
)
def update_project(
    project_id: int,
    project_data: ResearchProjectUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Cập nhật đề tài nghiên cứu.

    Chỉ OWNER mới được cập nhật.
    """

    project = update_research_project(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        project_data=project_data,
    )

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Cập nhật đề tài nghiên cứu thành công",
        data=ResearchProjectResponse.model_validate(project).model_dump(),
        request=request,
    )


# =========================================================
# TASK 4
# DELETE /research-projects/{project_id}
# =========================================================
@router.delete(
    "/{project_id}",
    status_code=status.HTTP_200_OK,
)
def delete_project(
    project_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Xóa đề tài nghiên cứu.

    Chỉ OWNER mới được xóa.
    """

    delete_research_project(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
    )

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Xóa đề tài nghiên cứu thành công",
        data=None,
        request=request,
    )
