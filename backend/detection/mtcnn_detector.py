import io

import numpy as np
from PIL import Image

from backend.utils.preprocessing import align_face, crop_face

_detector = None


def _get_detector():
    global _detector
    if _detector is None:
        from mtcnn import MTCNN

        _detector = MTCNN()
    return _detector


def read_image_from_bytes(image_bytes: bytes):
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    return np.array(image)


def detect_and_align(image_bytes: bytes):
    img = read_image_from_bytes(image_bytes)
    results = _get_detector().detect_faces(img)

    aligned_faces = []

    for result in results:
        box = result["box"]
        keypoints = result["keypoints"]

        crop_face(img, box)
        aligned = align_face(img, keypoints)

        aligned_faces.append(
            {
                "box": box,
                "confidence": result["confidence"],
                "aligned_face": aligned.tolist(),
            }
        )

    return aligned_faces


def detect_face(image_bytes: bytes):
    return detect_and_align(image_bytes)