from backend.database.database import Base, engine
from backend.database import models

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
