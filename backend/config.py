import os
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]

DATABASE_PATH = ROOT_DIR / "backend" / "database" / "attendance.db"
MODEL_PATH = ROOT_DIR / "models_local" / "facenet512.onnx"

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_PATH.as_posix()}")

MATCH_THRESHOLD = float(os.getenv("MATCH_THRESHOLD", "0.7"))
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES", str(5 * 1024 * 1024)))

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".gif",
    ".bmp",
    ".tif",
    ".tiff",
}

ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/jpg",
    "image/pjpeg",
    "image/png",
    "image/x-png",
    "image/webp",
    "image/gif",
    "image/bmp",
    "image/x-ms-bmp",
    "image/tiff",
    "image/x-tiff",
}

ADMIN_API_KEY = os.getenv("ADMIN_API_KEY", "")
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
RATE_LIMIT = os.getenv("RATE_LIMIT", "30/minute")
