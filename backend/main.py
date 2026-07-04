from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.register import router as register_router
from backend.api.recognize import router as recognize_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register_router, prefix="/register")
app.include_router(recognize_router, prefix="/recognize")
