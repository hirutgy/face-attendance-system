from typing import Annotated

from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from backend.auth import require_admin
from backend.database.crud import create_user
from backend.database.dp import get_db
from backend.recognition.pipeline import image_to_embedding
from backend.utils.validation import SUPPORTED_FORMATS_LABEL, read_validated_image

router = APIRouter()

NameField = Annotated[str, Form(description="Person's full name", examples=["Alice Smith"])]
PhotosField = Annotated[
    list[UploadFile],
    File(
        description=(
            f"Upload 1–5 face photos. Supported formats: {SUPPORTED_FORMATS_LABEL}. "
            "In Swagger UI, use the file picker — do not type text into this field."
        ),
    ),
]
PhotoField = Annotated[
    UploadFile,
    File(
        description=f"One face photo. Supported formats: {SUPPORTED_FORMATS_LABEL}.",
    ),
]


@router.post(
    "/register",
    summary="Register a user with face photos",
    response_description="Registration result with user id and embedding count",
)
async def register_user(
    name: NameField,
    files: PhotosField,
    db: Session = Depends(get_db),
    _: None = Depends(require_admin),
):
    if not files:
        return {"status": "error", "message": "At least one photo is required"}

    embeddings = []
    for upload in files:
        image_bytes = await read_validated_image(upload)
        embeddings.append(image_to_embedding(image_bytes))

    user = create_user(name=name, embeddings=embeddings, db=db)

    return {
        "status": "success",
        "message": f"User '{name}' registered with {len(embeddings)} photo(s)",
        "name": user.name,
        "user_id": user.id,
        "embeddings_added": len(embeddings),
    }
