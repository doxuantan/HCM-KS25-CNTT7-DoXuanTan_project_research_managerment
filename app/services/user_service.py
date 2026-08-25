from sqlalchemy.orm import Session

from app.models.user import User


def get_current_user(
    db: Session,
    user_id: int,
):
    """
    Lấy thông tin người dùng hiện tại theo user_id.
    """
    user = db.query(User).filter(User.id == user_id).first()
    return user


def get_users(
    db: Session,
    name: str | None = None,
    email: str | None = None,
    is_active: bool | None = None,
):
    """
    Lấy danh sách người dùng.
    Có thể tìm kiếm theo:
    - name
    - email
    - is_active
    """

    query = db.query(User)
    # Tìm theo tên
    if name:
        query = query.filter(User.full_name.ilike(f"%{name}%"))
    # Tìm theo email
    if email:
        query = query.filter(User.email.ilike(f"%{email}%"))
    # Lọc theo trạng thái
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    return query.all()
