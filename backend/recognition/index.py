import json
from threading import Lock

import numpy as np
from sqlalchemy.orm import Session, joinedload

from backend.database.models import Embedding
from backend.utils.similarity import batch_cosine_similarity


class EmbeddingIndex:
    """In-memory index for fast vector search across all stored embeddings."""

    def __init__(self) -> None:
        self._vectors: np.ndarray | None = None
        self._user_ids: list[int] = []
        self._lock = Lock()

    def refresh(self, db: Session) -> None:
        records = (
            db.query(Embedding)
            .options(joinedload(Embedding.user))
            .all()
        )

        if not records:
            with self._lock:
                self._vectors = None
                self._user_ids = []
            return

        vectors = []
        user_ids = []

        for record in records:
            vectors.append(json.loads(record.vector))
            user_ids.append(record.user_id)

        with self._lock:
            self._vectors = np.asarray(vectors, dtype=np.float32)
            self._user_ids = user_ids

        print("================================")
        print(f"Embedding index refreshed.")
        print(f"Users loaded: {len(self._user_ids)}")
        print("================================")

    def find_best_match(
        self,
        embedding: list,
        threshold: float,
    ) -> tuple[object | None, float]:

        with self._lock:
            if self._vectors is None or len(self._user_ids) == 0:
                print("Embedding index is EMPTY!")
                return None, -1.0

            vectors = self._vectors
            user_ids = self._user_ids

        scores = batch_cosine_similarity(embedding, vectors)
        best_idx = int(np.argmax(scores))
        best_score = float(scores[best_idx])
        best_user_id = user_ids[best_idx]

        print("================================")
        print("Similarity scores:", scores)
        print("Best score:", best_score)
        print("Threshold:", threshold)
        print("Matched user id:", best_user_id)
        print("================================")

        if best_score < threshold:
            print("No match: score below threshold.")
            return None, best_score

        print("Match found!")
        return best_user_id, best_score


embedding_index = EmbeddingIndex()