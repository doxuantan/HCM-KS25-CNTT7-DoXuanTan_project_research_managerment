from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.research_task import ResearchTask
from app.models.research_project import ResearchProject
from app.models.user import User

from app.schemas.research_task import (
    ResearchTaskCreate,
    ResearchTaskUpdate,
)

from app.core.validators import (
    check_project_member,
    check_user_in_project,
    validate_status,
    validate_priority,
)


# =========================================================
# TASK 1: Tạo nhiệm vụ nghiên cứu
# =========================================================
def create_research_task(
    db: Session,
    project_id: int,
    task_data: ResearchTaskCreate,
    user_id: int,
):
    """
    Thành viên tạo một nhiệm vụ nghiên cứu.
    """

    # 1. Kiểm tra user có thuộc project không
    check_project_member(
        db,
        project_id,
        user_id,
    )

    # 2. Kiểm tra tên task
    if not task_data.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tên nhiệm vụ không được để trống",
        )

    # 3. Kiểm tra status và priority
    validate_status(task_data.status)
    validate_priority(task_data.priority)

    # 4. Nếu có người được giao thì kiểm tra người đó
    if task_data.assignee_id is not None:

        user = (
            db.query(User)
            .filter(User.id == task_data.assignee_id)
            .first()
        )

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Người được giao không tồn tại",
            )

        if not check_user_in_project(
            db,
            project_id,
            task_data.assignee_id,
        ):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Người được giao không thuộc đề tài",
            )

    # 5. Tạo task
    new_task = ResearchTask(
        project_id=project_id,
        title=task_data.title.strip(),
        description=task_data.description,
        assignee_id=task_data.assignee_id,
        status=task_data.status,
        priority=task_data.priority,
        due_date=task_data.due_date,
    )

    # 6. Lưu database
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


# =========================================================
# TASK 2: Danh sách nhiệm vụ
# TASK 8: Search & Filter
# TASK 9: Pagination & Sort
# =========================================================
def get_research_tasks(
    db: Session,
    project_id: int,
    user_id: int,
    status_filter: str | None = None,
    priority: str | None = None,
    assignee_id: int | None = None,
    title: str | None = None,
    limit: int = 10,
    offset: int = 0,
    sort_by: str = "created_at",
):
    """
    Lấy danh sách task của một project.
    """

    # 1. Kiểm tra user có quyền xem project
    check_project_member(
        db,
        project_id,
        user_id,
    )

    # 2. Kiểm tra pagination
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit phải từ 1 đến 100",
        )

    if offset < 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Offset không được nhỏ hơn 0",
        )

    # 3. Kiểm tra filter
    if status_filter:
        validate_status(status_filter)

    if priority:
        validate_priority(priority)

    # 4. Kiểm tra sort
    if sort_by not in ["created_at", "due_date"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Sort không hợp lệ",
        )

    # 5. Chỉ lấy task của project hiện tại
    query = (
        db.query(ResearchTask)
        .filter(ResearchTask.project_id == project_id)
    )
    # 6. Filter status
    if status_filter:
        query = query.filter(
            ResearchTask.status == status_filter
        )
    # 7. Filter priority
    if priority:
        query = query.filter(
            ResearchTask.priority == priority
        )
    # 8. Filter assignee
    if assignee_id is not None:
        query = query.filter(
            ResearchTask.assignee_id == assignee_id
        )
    # 9. Search theo title
    if title:
        query = query.filter(
            ResearchTask.title.ilike(f"%{title}%")
        )
    # 10. Đếm tổng số task
    total = query.count()

    # 11. Sort
    if sort_by == "due_date":
        query = query.order_by(
            ResearchTask.due_date
        )
    else:
        query = query.order_by(
            ResearchTask.created_at.desc()
        )
    # 12. Phân trang
    tasks = (
        query
        .offset(offset)
        .limit(limit)
        .all()
    )
    return {
        "items": tasks,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


# =========================================================
# TASK 3: Chi tiết nhiệm vụ
# =========================================================
def get_research_task_detail(
    db: Session,
    task_id: int,
    user_id: int,
):
    """
    Lấy chi tiết một task.
    User phải thuộc project của task.
    """

    # 1. Tìm task
    task = (
        db.query(ResearchTask)
        .filter(ResearchTask.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nhiệm vụ nghiên cứu không tồn tại",
        )

    # 2. Kiểm tra user thuộc project
    check_project_member(
        db,
        task.project_id,
        user_id,
    )

    return task


# =========================================================
# TASK 4: Cập nhật nhiệm vụ
# TASK 6: Giao việc
# TASK 7: Workflow
# =========================================================
def update_research_task(
    db: Session,
    task_id: int,
    user_id: int,
    task_data: ResearchTaskUpdate,
):
    """
    OWNER hoặc ASSIGNEE được cập nhật task.

    Chỉ cập nhật field được gửi lên.
    """

    # 1. Tìm task
    task = (
        db.query(ResearchTask)
        .filter(ResearchTask.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nhiệm vụ nghiên cứu không tồn tại",
        )

    # 2. Tìm project của task
    project = (
        db.query(ResearchProject)
        .filter(
            ResearchProject.id == task.project_id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đề tài nghiên cứu không tồn tại",
        )

    # 3. Chỉ OWNER hoặc ASSIGNEE được sửa
    if (
        project.owner_id != user_id
        and task.assignee_id != user_id
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền cập nhật nhiệm vụ",
        )

    # 4. Lấy những field client thực sự gửi lên
    update_data = task_data.model_dump(
        exclude_unset=True
    )

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không có dữ liệu để cập nhật",
        )

    # 5. Kiểm tra title
    if "title" in update_data:

        if not update_data["title"].strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tên nhiệm vụ không được để trống",
            )

        update_data["title"] = (
            update_data["title"].strip()
        )

    # 6. Kiểm tra status
    if "status" in update_data:
        validate_status(
            update_data["status"]
        )

    # 7. Kiểm tra priority
    if "priority" in update_data:
        validate_priority(
            update_data["priority"]
        )

    # 8. Nếu đổi assignee thì kiểm tra user
    if "assignee_id" in update_data:

        new_assignee_id = update_data["assignee_id"]

        if new_assignee_id is not None:

            user = (
                db.query(User)
                .filter(User.id == new_assignee_id)
                .first()
            )

            if user is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Người được giao không tồn tại",
                )

            if not check_user_in_project(
                db,
                task.project_id,
                new_assignee_id,
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Người được giao không thuộc đề tài",
                )

    # 9. Cập nhật các field
    for field, value in update_data.items():
        setattr(task, field, value)

    # 10. Lưu database
    db.commit()
    db.refresh(task)

    return task


# =========================================================
# TASK 5: Xóa nhiệm vụ
# =========================================================
def delete_research_task(
    db: Session,
    task_id: int,
    user_id: int,
):
    """
    Chỉ OWNER được xóa task.
    """

    # 1. Tìm task
    task = (
        db.query(ResearchTask)
        .filter(ResearchTask.id == task_id)
        .first()
    )

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nhiệm vụ nghiên cứu không tồn tại",
        )

    # 2. Tìm project
    project = (
        db.query(ResearchProject)
        .filter(
            ResearchProject.id == task.project_id
        )
        .first()
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Đề tài nghiên cứu không tồn tại",
        )

    # 3. Chỉ OWNER được xóa
    if project.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chỉ OWNER mới được xóa nhiệm vụ",
        )

    # 4. Xóa task
    db.delete(task)
    db.commit()

    return True