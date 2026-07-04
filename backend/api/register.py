from fastapi import APIRouter, UploadFile, File, Form
from backend.detection.mtcnn_detector import detect_face
from backend.models.facenet_model import get_embedding
from backend.database.crud import create_user
import numpy as np
from PIL import Image
import io

router = APIRouter()

@router.post("/register")
async def register_user(
    name: str = Form(...),
    file: UploadFile = File(...)
):
    # Read image bytes
    image_bytes = await file.read()

    # Detect + align face
    faces = detect_face(image_bytes)

    if len(faces) == 0:
        return {"error": "No face detected"}

    # Use the first detected face
    aligned_face = np.array(faces[0]["aligned_face"], dtype=np.float32)

    # Generate embedding
    embedding = get_embedding(aligned_face)

    # Save to DB
    create_user(name=name, embedding=embedding)

    return {
        "status": "success",
        "name": name,
        "embedding_dim": len(embedding)
    }
