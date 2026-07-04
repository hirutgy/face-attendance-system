import numpy as np
from fastapi import HTTPException

from backend.detection.mtcnn_detector import detect_face
from backend.models.facenet_model import get_embedding


def image_to_embedding(image_bytes: bytes) -> list:
    faces = detect_face(image_bytes)
    if not faces:
        raise HTTPException(status_code=422, detail="No face detected")

    aligned_face = np.array(faces[0]["aligned_face"], dtype=np.float32)
    return get_embedding(aligned_face)
