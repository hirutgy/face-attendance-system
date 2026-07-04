from typing import Annotated

from fastapi import APIRouter, UploadFile, File

from backend.detection.mtcnn_detector import detect_and_align
from backend.utils.validation import SUPPORTED_FORMATS_LABEL, read_validated_image

router = APIRouter()

PhotoField = Annotated[
    UploadFile,
    File(description=f"Image to detect faces in. Formats: {SUPPORTED_FORMATS_LABEL}."),
]


@router.post("/", summary="Detect faces in an image")
async def detect_faces(image: PhotoField):
    image_bytes = await read_validated_image(image)
    faces = detect_and_align(image_bytes)

    return {
        "num_faces": len(faces),
        "faces": faces,
    }
