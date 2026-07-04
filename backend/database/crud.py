import json

from sqlalchemy.orm import Session
from datetime import datetime, date

from backend.database.models import User, Attendance, Embedding
from backend.database.database import SessionLocal
from backend.recognition.index import embedding_index


def log_attendance(db: Session, user_id: int, confidence: float):
    entry = Attendance(
        user_id=user_id,
        confidence=confidence,
        timestamp=datetime.now(),
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def has_checked_in_today(db: Session, user_id: int) -> bool:
    today = date.today()
    start = datetime.combine(today, datetime.min.time())
    existing = (
        db.query(Attendance)
        .filter(Attendance.user_id == user_id, Attendance.timestamp >= start)
        .first()
    )
    return existing is not None


def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()


def create_user(name: str, embeddings: list[list], db: Session | None = None):
    own_session = db is None
    if own_session:
        db = SessionLocal()

    try:
        user = db.query(User).filter(User.name == name).first()
        if user is None:
            user = User(name=name)
            db.add(user)
            db.flush()

        for embedding in embeddings:
            db.add(
                Embedding(
                    user_id=user.id,
                    vector=json.dumps(embedding),
                    model_type="facenet512",
                )
            )

        db.commit()
        db.refresh(user)
        embedding_index.refresh(db)
        return user
    finally:
        if own_session:
            db.close()


def get_user_profile(db: Session, user_id: int) -> dict | None:
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        return None

    records = (
        db.query(Attendance)
        .filter(Attendance.user_id == user_id)
        .order_by(Attendance.timestamp.desc())
        .all()
    )

    total = len(records)
    avg_conf = sum(r.confidence for r in records) / total if total else 0.0

    return {
        "id": user.id,
        "name": user.name,
        "total_entries": total,
        "average_confidence": avg_conf,
        "latest_checkins": [
            {
                "timestamp": r.timestamp.isoformat(),
                "confidence": r.confidence,
            }
            for r in records[:10]
        ],
    }
