import io
from pathlib import Path

from fastapi import HTTPException, UploadFile
from PIL import Image, UnidentifiedImageError

from backend.config import (
    ALLOWED_IMAGE_EXTENSIONS,
    ALLOWED_IMAGE_TYPES,
    MAX_UPLOAD_BYTES,
)

SUPPORTED_FORMATS_LABEL = "JPG, JPEG, PNG, WebP, GIF, BMP, TIFF"


def is_allowed_image(filename: str | None, content_type: str | None) -> bool:
    if content_type and content_type.lower() in ALLOWED_IMAGE_TYPES:
        return True
    if filename:
        ext = Path(filename).suffix.lower()
        return ext in ALLOWED_IMAGE_EXTENSIONS
    return False


def verify_image_bytes(data: bytes) -> None:
    try:
        with Image.open(io.BytesIO(data)) as img:
            img.verify()
    except (UnidentifiedImageError, OSError, SyntaxError) as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid or unsupported image file. Use {SUPPORTED_FORMATS_LABEL}.",
        ) from exc


async def read_validated_image(file: UploadFile) -> bytes:
    if not is_allowed_image(file.filename, file.content_type):
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported image type: {file.content_type or Path(file.filename or '').suffix or 'unknown'}. "
                f"Allowed formats: {SUPPORTED_FORMATS_LABEL}."
            ),
        )

    data = await file.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file uploaded")

    if len(data) > MAX_UPLOAD_BYTES:
        raise HTTPException(
            status_code=400,
            detail=f"File too large (max {MAX_UPLOAD_BYTES // (1024 * 1024)} MB)",
        )

    verify_image_bytes(data)
    return data
