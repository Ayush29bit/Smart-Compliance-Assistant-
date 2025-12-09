from fastapi import APIRouter
from app.services.rag_pipeline import run_rag

router = APIRouter()

@router.post("/query")
async def query_rag(payload: dict):
    query = payload["query"]
    answer = run_rag(query)
    return {"answer": answer}
