from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.database.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    embeddings = relationship("Embedding", back_populates="user", cascade="all, delete-orphan")
    attendance = relationship("Attendance", back_populates="user", cascade="all, delete-orphan")


class Embedding(Base):
    __tablename__ = "embeddings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    vector = Column(String, nullable=False)
    model_type = Column(String, default="facenet512")

    user = relationship("User", back_populates="embeddings")

    __table_args__ = (Index("ix_embeddings_user_model", "user_id", "model_type"),)


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)

    user = relationship("User", back_populates="attendance")

    __table_args__ = (Index("ix_attendance_user_timestamp", "user_id", "timestamp"),)
