import numpy as np
from sqlalchemy.orm import Session
from backend.database.models import User

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def find_best_match(db: Session, embedding: list, threshold: float = 0.7):
    users = db.query(User).all()

    best_user = None
    best_score = -1

    for user in users:
        score = cosine_similarity(embedding, user.embedding)
        if score > best_score:
            best_score = score
            best_user = user

    if best_score < threshold:
        return None, best_score

    return best_user, best_score
