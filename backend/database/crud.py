from sqlalchemy.orm import Session
from datetime import datetime

from backend.database.models import User, Attendance
from backend.database.database import SessionLocal


def log_attendance(db: Session, user_id: int, confidence: float):
    entry = Attendance(
        user_id=user_id,
        confidence=confidence,
        timestamp=datetime.now()
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_user_by_embedding(db: Session, identity: str):
    return db.query(User).filter(User.name == identity).first()


def create_user(name: str, embedding: list):
    db = SessionLocal()
    user = User(name=name, embedding=embedding)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user
