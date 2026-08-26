from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User

from app.schemas.research_task import (
    ResearchTaskCreate,
    ResearchTaskUpdate,
    ResearchTaskResponse,
)

from app.core.dependencies import get_current_user
from app.core.responses import success_full

from app.services.research_task_service import (
    create_research_task,
    get_research_tasks,
    get_research_task_detail,
    update_research_task,
    delete_research_task,
)


router = APIRouter(
    tags=["Research Task"],
)


# =========================================================
# TASK 1: Tạo nhiệm vụ nghiên cứu
# POST /research-projects/{project_id}/research-tasks
# =========================================================
@router.post(
    "/research-projects/{project_id}/research-tasks",
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    project_id: int,
    task_data: ResearchTaskCreate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Thành viên tạo nhiệm vụ nghiên cứu.
    """

    new_task = create_research_task(
        db=db,
        project_id=project_id,
        task_data=task_data,
        user_id=current_user.id,
    )

    return success_full(
        statusCode=status.HTTP_201_CREATED,
        message="Tạo nhiệm vụ nghiên cứu thành công",
        data=ResearchTaskResponse.model_validate(
            new_task
        ).model_dump(),
        request=request,
    )


# =========================================================
# TASK 2: Danh sách nhiệm vụ
# TASK 8: Search & Filter
# TASK 9: Pagination & Sort
# GET /research-projects/{project_id}/research-tasks
# =========================================================
@router.get(
    "/research-projects/{project_id}/research-tasks",
    status_code=status.HTTP_200_OK,
)
def get_task_list(
    project_id: int,
    request: Request,
    status_filter: str | None = None,
    priority: str | None = None,
    assignee_id: int | None = None,
    title: str | None = None,
    page: int = 1,
    size: int = 10,
    sort_by: str = "created_at",
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Lấy danh sách nhiệm vụ của project.

    Có thể:
    - lọc theo status
    - lọc theo priority
    - lọc theo assignee
    - tìm kiếm theo title
    - phân trang
    - sắp xếp
    """

    result = get_research_tasks(
        db=db,
        project_id=project_id,
        user_id=current_user.id,
        status_filter=status_filter,
        priority=priority,
        assignee_id=assignee_id,
        title=title,
        page=page,
        size=size,
        sort_by=sort_by,
    )

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Lấy danh sách nhiệm vụ thành công",
        data={
            "items": [
                ResearchTaskResponse.model_validate(
                    task
                ).model_dump()
                for task in result["items"]
            ],
            "total": result["total"],
            "page": result["page"],
            "size": result["size"],
        },
        request=request,
    )


# =========================================================
# TASK 3: Chi tiết nhiệm vụ
# GET /research-tasks/{task_id}
# =========================================================
@router.get(
    "/research-tasks/{task_id}",
    status_code=status.HTTP_200_OK,
)
def get_task_detail(
    task_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Lấy chi tiết nhiệm vụ.
    User phải thuộc project của task.
    """

    task = get_research_task_detail(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Lấy chi tiết nhiệm vụ thành công",
        data=ResearchTaskResponse.model_validate(
            task
        ).model_dump(),
        request=request,
    )


# =========================================================
# TASK 4: Cập nhật nhiệm vụ
# TASK 6: Giao việc
# TASK 7: Workflow
# PATCH /research-tasks/{task_id}
# =========================================================
@router.patch(
    "/research-tasks/{task_id}",
    status_code=status.HTTP_200_OK,
)
def update_task(
    task_id: int,
    task_data: ResearchTaskUpdate,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Cập nhật nhiệm vụ.

    OWNER hoặc ASSIGNEE được cập nhật.
    """

    task = update_research_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
        task_data=task_data,
    )

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Cập nhật nhiệm vụ thành công",
        data=ResearchTaskResponse.model_validate(
            task
        ).model_dump(),
        request=request,
    )


# =========================================================
# TASK 5: Xóa nhiệm vụ
# DELETE /research-tasks/{task_id}
# =========================================================
@router.delete(
    "/research-tasks/{task_id}",
    status_code=status.HTTP_200_OK,
)
def delete_task(
    task_id: int,
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Xóa nhiệm vụ.
    Chỉ OWNER được xóa.
    """

    delete_research_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
    )

    return success_full(
        statusCode=status.HTTP_200_OK,
        message="Xóa nhiệm vụ thành công",
        data=None,
        request=request,
    )