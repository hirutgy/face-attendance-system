from fastapi import APIRouter, UploadFile, File
from backend.detection.mtcnn_detector import detect_and_align

router = APIRouter()

@router.post("/")
async def detect_face(image: UploadFile = File(...)):
    image_bytes = await image.read()
    faces = detect_and_align(image_bytes)

    return {
        "num_faces": len(faces),
        "faces": faces
    }
