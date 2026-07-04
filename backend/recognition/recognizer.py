"""Legacy wrapper — use backend.recognition.engine.find_best_match instead."""

from backend.recognition.engine import find_best_match
from backend.recognition.pipeline import image_to_embedding

__all__ = ["find_best_match", "image_to_embedding"]
