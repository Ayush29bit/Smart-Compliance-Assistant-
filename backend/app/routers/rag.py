from fastapi import APIRouter, HTTPException
from app.services.rag_pipeline import run_rag
import logging

router = APIRouter()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/query")
async def query_rag(payload: dict):
    try:
        query = payload["query"]
        logger.info(f"Received query: {query}")
        
        # Run the RAG pipeline
        answer = run_rag(query)
        logger.info(f"Generated answer: {answer[:100]}...")  # Log first 100 chars
        
        return {"answer": answer}
    
    except KeyError:
        logger.error("Query field missing in payload")
        raise HTTPException(status_code=400, detail="Query field is required")
    
    except Exception as e:
        logger.error(f"Error in query_rag: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing query: {str(e)}")
