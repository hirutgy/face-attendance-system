from collections import defaultdict
from datetime import datetime

from sqlalchemy.orm import Session

from backend.database.models import Attendance, User


def compute_analytics(db: Session) -> dict:
    records = (
        db.query(Attendance)
        .join(User)
        .order_by(Attendance.timestamp.desc())
        .all()
    )

    total_entries = len(records)
    per_person: dict[str, int] = defaultdict(int)
    per_day: dict[str, int] = defaultdict(int)

    for record in records:
        per_person[record.user.name] += 1
        day = record.timestamp.date().isoformat()
        per_day[day] += 1

    latest = [
        {
            "name": record.user.name,
            "confidence": record.confidence,
            "timestamp": record.timestamp.isoformat(),
        }
        for record in records[:10]
    ]

    avg_conf = (
        sum(record.confidence for record in records) / total_entries
        if total_entries
        else 0.0
    )

    return {
        "total_entries": total_entries,
        "per_person": dict(per_person),
        "per_day": dict(per_day),
        "latest_checkins": latest,
        "average_confidence": avg_conf,
    }
