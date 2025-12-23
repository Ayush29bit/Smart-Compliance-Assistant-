from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, upload
from app.routers import rag


app = FastAPI(title="Smart Compliance Assistant - Backend")

# CORS Middleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(health.router, prefix="/api")
app.include_router(upload.router, prefix="/api")
app.include_router(rag.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Smart Compliance Assistant Backend!"}