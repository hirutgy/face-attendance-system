from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
import numpy as np

from backend.database.database import SessionLocal
from backend.database import crud
from backend.detection.mtcnn_detector import detect_and_align
from backend.models.facenet_model import get_embedding

from backend.recognition.recognizer import recognize_face

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
async def mark_attendance(image: UploadFile = File(...), db: Session = Depends(get_db)):
    image_bytes = await image.read()

    # detect + align
    faces = detect_and_align(image_bytes)
    if len(faces) == 0:
        raise HTTPException(status_code=400, detail="No face detected")

    aligned = np.array(faces[0]["aligned_face"])

    # embedding
    embedding = get_embedding(aligned)

    # recognition
    result = recognize_face(embedding)
    identity = result["identity"]
    confidence = result["confidence"]

    # find user in DB
    user = crud.get_user_by_name(db, identity)
    if not user:
        raise HTTPException(status_code=404, detail="User not registered")

    # log attendance
    entry = crud.log_attendance(db, user.id, confidence)

    return {
        "status": "attendance logged",
        "user": identity,
        "confidence": confidence,
        "timestamp": entry.timestamp.isoformat()
    }
