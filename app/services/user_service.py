from sqlalchemy.orm import Session

from app.models.user import User


def get_users(
    db: Session,
    name: str | None = None,
    email: str | None = None,
    is_active: bool | None = None,
):
    """
    Lấy danh sách người dùng.
    """

    query = db.query(User)

    if name:
        query = query.filter(
            User.full_name.ilike(f"%{name}%")
        )

    if email:
        query = query.filter(
            User.email.ilike(f"%{email}%")
        )

    if is_active is not None:
        query = query.filter(
            User.is_active == is_active
        )

    return query.all()