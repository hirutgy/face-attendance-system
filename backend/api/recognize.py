from typing import Annotated
import traceback

from fastapi import APIRouter, UploadFile, File, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from backend.database.crud import log_attendance
from backend.database.dp import get_db
from backend.recognition.engine import find_best_match
from backend.recognition.pipeline import image_to_embedding
from backend.utils.validation import (
    SUPPORTED_FORMATS_LABEL,
    read_validated_image,
)

router = APIRouter()

PhotoField = Annotated[
    UploadFile,
    File(description=f"Face photo to identify. Formats: {SUPPORTED_FORMATS_LABEL}."),
]


@router.post("/", summary="Recognize a face")
async def recognize(
    file: PhotoField,
    log: bool = Query(default=False),
    db: Session = Depends(get_db),
):
    try:
        print("=== START RECOGNITION ===")

        image_bytes = await read_validated_image(file)
        print("✓ Image read")

        embedding = image_to_embedding(image_bytes)
        print("✓ Embedding created")

        best_match, confidence = find_best_match(db, embedding)
        print("✓ Match search complete")

        if best_match is None:
            return {
                "status": "error",
                "message": "No matching user found",
                "confidence": confidence,
            }

        response = {
            "status": "success",
            "name": best_match.name,
            "user_id": best_match.id,
            "confidence": confidence,
        }

        if log:
            entry = log_attendance(db, best_match.id, confidence)
            response["attendance_logged"] = True
            response["timestamp"] = entry.timestamp.isoformat()

        return response

    except HTTPException:
        raise

    except Exception:
        print("\n========== EXCEPTION ==========")
        traceback.print_exc()
        print("===============================\n")

        raise HTTPException(
            status_code=422,
            detail="Face processing failed. Use a clear, front-facing image.",
        )