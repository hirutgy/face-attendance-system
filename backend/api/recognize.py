from fastapi import APIRouter, UploadFile, File
from backend.models.facenet_model import get_embedding
from backend.database.database import SessionLocal
from backend.database.models import User
from backend.detection.mtcnn_detector import detect_face

router = APIRouter()

@router.post("/")
async def recognize(image: UploadFile = File(...)):
    # Read image bytes
    img_bytes = await image.read()

    # Detect face
    face = detect_face(img_bytes)
    if face is None:
        return {"status": "error", "message": "No face detected"}

    # Generate embedding
    embedding = get_embedding(face)

    # Compare with DB
    db = SessionLocal()
    users = db.query(User).all()

    best_match = None
    best_distance = 999

    for user in users:
        dist = sum((e1 - e2)**2 for e1, e2 in zip(embedding, user.embedding))
        if dist < best_distance:
            best_distance = dist
            best_match = user

    db.close()

    if best_match is None:
        return {"status": "error", "message": "No users in database"}

    return {
        "status": "success",
        "name": best_match.name,
        "distance": best_distance
    }
