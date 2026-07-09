from datetime import date, datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.database.dp import get_db
from backend.database.models import Attendance, User

router = APIRouter()


class ChatRequest(BaseModel):
    message: str


def get_today_start() -> datetime:
    today = date.today()
    return datetime.combine(today, datetime.min.time())


def get_today_attendance(db: Session) -> str:
    start = get_today_start()

    records = (
        db.query(Attendance)
        .join(User, Attendance.user_id == User.id)
        .filter(Attendance.timestamp >= start)
        .order_by(Attendance.timestamp.desc())
        .all()
    )

    if not records:
        return "No students have checked in today yet."

    lines = ["Today's attendance records:\n"]

    for record in records:
        name = record.user.name if record.user else f"User ID {record.user_id}"
        time = record.timestamp.strftime("%I:%M %p")
        confidence = round(record.confidence * 100, 1)
        lines.append(f"• {name} — {time} — {confidence}% confidence")

    lines.append(f"\nTotal present today: {len(records)} student(s).")
    return "\n".join(lines)


def get_all_users(db: Session) -> str:
    users = db.query(User).order_by(User.name).all()

    if not users:
        return "No registered students were found."

    lines = ["Registered students:\n"]

    for user in users:
        lines.append(f"• {user.name}")

    lines.append(f"\nTotal registered: {len(users)}")
    return "\n".join(lines)


def get_attendance_analytics(db: Session) -> str:
    total_users = db.query(User).count()
    total_attendance = db.query(Attendance).count()

    start = get_today_start()

    today_attendance = (
        db.query(Attendance)
        .filter(Attendance.timestamp >= start)
        .count()
    )

    confidence_records = db.query(Attendance.confidence).all()

    if confidence_records:
        avg_confidence = (
            sum(record[0] for record in confidence_records)
            / len(confidence_records)
        )
        avg_confidence_percent = round(avg_confidence * 100, 1)
    else:
        avg_confidence_percent = 0

    attendance_rate = (
        round((today_attendance / total_users) * 100, 1)
        if total_users
        else 0
    )

    return (
        "Attendance Analytics:\n\n"
        f"• Registered students: {total_users}\n"
        f"• Check-ins today: {today_attendance}\n"
        f"• Total attendance records: {total_attendance}\n"
        f"• Today's attendance rate: {attendance_rate}%\n"
        f"• Average confidence: {avg_confidence_percent}%"
    )


def get_absent_today(db: Session) -> str:
    start = get_today_start()
    all_users = db.query(User).order_by(User.name).all()

    if not all_users:
        return "No registered students were found."

    present_user_ids = {
        record.user_id
        for record in db.query(Attendance)
        .filter(Attendance.timestamp >= start)
        .all()
    }

    present_users = [user for user in all_users if user.id in present_user_ids]
    absent_users = [user for user in all_users if user.id not in present_user_ids]

    if not absent_users:
        return (
            "Everyone is present today.\n\n"
            f"Present today: {len(present_users)} / {len(all_users)} students\n"
            "Attendance rate: 100%"
        )

    attendance_rate = round((len(present_users) / len(all_users)) * 100, 1)

    lines = ["Absent today:\n"]
    for user in absent_users:
        lines.append(f"• {user.name}")

    lines.append(f"\nPresent today: {len(present_users)} / {len(all_users)} students")
    lines.append(f"Attendance rate: {attendance_rate}%")

    return "\n".join(lines)


@router.post("/chat")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    message = request.message.lower().strip()

    if "hello" in message or message == "hi":
        return {"reply": "Hello! I'm your Face Attendance AI Assistant."}

    if (
        "attended today" in message
        or "who attended" in message
        or "present today" in message
    ):
        return {"reply": get_today_attendance(db)}

    if "absent" in message or "missing" in message or "not here" in message:
        return {"reply": get_absent_today(db)}

    if "analytics" in message or "summary" in message or "stats" in message:
        return {"reply": get_attendance_analytics(db)}

    if "users" in message or "students" in message or "registered" in message:
        return {"reply": get_all_users(db)}

    if "register" in message or "add student" in message or "new student" in message:
        return {
            "reply": (
                "To register a new student:\n\n"
                "1. Go to the Register page.\n"
                "2. Enter the student's full name.\n"
                "3. Upload 1–5 clear face images.\n"
                "4. Click Register Student.\n\n"
                "After registration, the student is saved in the database and can be used for recognition and attendance."
            )
        }

    if "recognize" in message or "identify" in message or "face match" in message:
        return {
            "reply": (
                "To recognize a student:\n\n"
                "1. Go to the Recognize page.\n"
                "2. Upload a clear face image.\n"
                "3. Choose Recognize Only to identify the student.\n"
                "4. Choose Mark Attendance to record attendance after recognition.\n\n"
                "The system compares the uploaded face against registered student embeddings."
            )
        }

    return {
        "reply": (
            "I can help with attendance questions. Try asking:\n\n"
            "• Who attended today?\n"
            "• Who is absent today?\n"
            "• Show all registered users.\n"
            "• Show attendance analytics.\n"
            "• How do I register a new student?\n"
            "• Recognize a student."
        )
    }