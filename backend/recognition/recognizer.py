import numpy as np
import json

def load_embeddings():
    with open("backend/database/embeddings.json", "r") as f:
        return json.load(f)

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def recognize_face(embedding, threshold=0.75):
    """
    embedding: 128-d FaceNet embedding
    threshold: similarity threshold (higher = stricter)
    """
    db = load_embeddings()

    best_match = None
    best_score = -1

    for name, stored_embedding in db.items():
        score = cosine_similarity(embedding, stored_embedding)

        if score > best_score:
            best_score = score
            best_match = name

    if best_score >= threshold:
        return {
            "identity": best_match,
            "confidence": float(best_score)
        }
    else:
        return {
            "identity": "unknown",
            "confidence": float(best_score)
        }
