from fastapi import APIRouter
from backend.attendance.analytics import compute_analytics

router = APIRouter()

@router.get("/")
def attendance_analytics():
    data = compute_analytics()
    return data
