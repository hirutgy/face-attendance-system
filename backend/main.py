from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address

from backend.api.analytics import router as analytics_router
from backend.api.attendance import router as attendance_router
from backend.api.detect import router as detect_router
from backend.api.embed import router as embed_router
from backend.api.recognize import router as recognize_router
from backend.api.register import router as register_router
from backend.api.users import router as users_router
from backend.config import CORS_ORIGINS, MODEL_PATH, RATE_LIMIT
from backend.database.database import SessionLocal
from backend.database.init_db import init_db
from backend.openapi import setup_openapi
from backend.recognition.index import embedding_index

limiter = Limiter(key_func=get_remote_address, default_limits=[RATE_LIMIT])


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        embedding_index.refresh(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Face Attendance System", lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register_router, prefix="/register", tags=["register"])
app.include_router(recognize_router, prefix="/recognize", tags=["recognize"])
app.include_router(attendance_router, prefix="/attendance", tags=["attendance"])
app.include_router(analytics_router, prefix="/attendance/analytics", tags=["analytics"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(detect_router, prefix="/detect", tags=["detect"])
app.include_router(embed_router, prefix="/embed", tags=["embed"])

setup_openapi(app)


@app.get("/health")
@limiter.limit("60/minute")
def health(request: Request):
    return {
        "status": "ok",
        "model_present": MODEL_PATH.exists(),
    }
