from datetime import datetime, date
from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session

from backend.database.crud import has_checked_in_today, log_attendance
from backend.database.dp import get_db
from backend.database.models import Attendance, User
from backend.recognition.engine import find_best_match
from backend.recognition.pipeline import image_to_embedding
from backend.utils.validation import SUPPORTED_FORMATS_LABEL, read_validated_image

router = APIRouter()

PhotoField = Annotated[
    UploadFile,
    File(description=f"Face photo for check-in. Formats: {SUPPORTED_FORMATS_LABEL}."),
]


@router.post("/", summary="Mark attendance from a face photo")
async def mark_attendance(
    file: PhotoField,
    db: Session = Depends(get_db),
):
    image_bytes = await read_validated_image(file)
    embedding = image_to_embedding(image_bytes)
    user, confidence = find_best_match(db, embedding)

    if user is None:
        return {
            "status": "error",
            "message": "Unknown face",
            "confidence": confidence,
        }

    if has_checked_in_today(db, user.id):
        return {
            "status": "success",
            "name": user.name,
            "confidence": confidence,
            "message": "Already checked in today",
            "duplicate": True,
        }

    entry = log_attendance(db, user.id, confidence)
    return {
        "status": "success",
        "name": user.name,
        "confidence": confidence,
        "timestamp": entry.timestamp.isoformat(),
        "duplicate": False,
    }


@router.get("/all")
def get_attendance_records(db: Session = Depends(get_db)):
    records = (
        db.query(Attendance)
        .join(User)
        .order_by(Attendance.timestamp.desc())
        .all()
    )
    return {
        "records": [
            {
                "user_id": record.user_id,
                "name": record.user.name,
                "time": record.timestamp.isoformat(),
                "status": "present",
                "confidence": record.confidence,
            }
            for record in records
        ]
    }


@router.get("/today")
def get_today_attendance(db: Session = Depends(get_db)):
    today = date.today()
    records = (
        db.query(Attendance)
        .join(User)
        .filter(Attendance.timestamp >= datetime.combine(today, datetime.min.time()))
        .order_by(Attendance.timestamp.desc())
        .all()
    )
    return {
        "records": [
            {
                "user_id": record.user_id,
                "name": record.user.name,
                "time": record.timestamp.isoformat(),
                "status": "present",
                "confidence": record.confidence,
            }
            for record in records
        ]
    }
