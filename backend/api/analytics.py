from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.attendance.analytics import compute_analytics
from backend.database.dp import get_db

router = APIRouter()


@router.get("/")
def attendance_analytics(db: Session = Depends(get_db)):
    return compute_analytics(db)
