from backend.database.database import SessionLocal
from backend.database.models import User

def register_face(name: str, embedding: list):
    db = SessionLocal()

    user = User(name=name, embedding=embedding)
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()

    return {
        "status": "success",
        "name": name,
        "embedding_dim": len(embedding)
    }
