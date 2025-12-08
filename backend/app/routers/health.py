from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

router = APIRouter()

class HealthResponse(BaseModel):
    status: str
    details: dict[str, Any] = {}

@router.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "ok", "details": {"db": "unknown", "redis": "unknown"}}
