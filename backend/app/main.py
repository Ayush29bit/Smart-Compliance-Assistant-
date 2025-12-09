from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, upload
from app.routers import rag


app = FastAPI(title="Smart Compliance Assistant - Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(rag.router, prefix="/api")

