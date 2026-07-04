from typing import Annotated

from fastapi import APIRouter, UploadFile, File

from backend.recognition.pipeline import image_to_embedding
from backend.utils.validation import SUPPORTED_FORMATS_LABEL, read_validated_image

router = APIRouter()

PhotoField = Annotated[
    UploadFile,
    File(description=f"Face photo to embed. Formats: {SUPPORTED_FORMATS_LABEL}."),
]


@router.post("/", summary="Generate a face embedding")
async def embed_face(file: PhotoField):
    image_bytes = await read_validated_image(file)
    embedding = image_to_embedding(image_bytes)
    return {"embedding_dim": len(embedding), "embedding": embedding}
