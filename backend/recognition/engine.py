from sqlalchemy.orm import Session

from backend.config import MATCH_THRESHOLD
from backend.database.models import User
from backend.recognition.index import embedding_index


def find_best_match(
    db: Session,
    embedding: list,
    threshold: float = MATCH_THRESHOLD,
) -> tuple[User | None, float]:
    user_id, score = embedding_index.find_best_match(embedding, threshold)
    if user_id is None:
        return None, score

    user = db.query(User).filter(User.id == user_id).first()
    return user, score
