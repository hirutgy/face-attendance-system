from fastapi import APIRouter, UploadFile, File
from backend.models.facenet_model import get_embedding
import numpy as np
from PIL import Image

router = APIRouter()

@router.post("/embed")
async def embed_face(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")
    image = np.array(image)
    embedding = get_embedding(image)
    return {"embedding": embedding}
