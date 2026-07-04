from sqlalchemy.orm import Session

from backend.database.crud import log_attendance as db_log_attendance


def log_attendance(name: str, confidence: float, db: Session):
    """Deprecated JSON logger — use database crud.log_attendance instead."""
    from backend.database.crud import get_user_by_name

    user = get_user_by_name(db, name)
    if user is None:
        raise ValueError(f"Unknown user: {name}")
    return db_log_attendance(db, user.id, confidence)
