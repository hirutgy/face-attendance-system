from mtcnn import MTCNN
from PIL import Image
import numpy as np
import io

from backend.utils.preprocessing import crop_face, align_face

detector = MTCNN()

def read_image_from_bytes(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return np.array(image)

def detect_and_align(image_bytes: bytes):
    img = read_image_from_bytes(image_bytes)
    results = detector.detect_faces(img)

    aligned_faces = []

    for r in results:
        box = r["box"]
        keypoints = r["keypoints"]

        cropped = crop_face(img, box)
        aligned = align_face(img, keypoints)

        aligned_faces.append({
            "box": box,
            "confidence": r["confidence"],
            "aligned_face": aligned.tolist()
        })

    return aligned_faces

# ⭐ Add this wrapper so FastAPI can import detect_face
def detect_face(image_bytes: bytes):
    return detect_and_align(image_bytes)
