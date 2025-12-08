from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel

router = APIRouter()

class UploadResponse(BaseModel):
    filename: str
    status: str

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    # For now, just accept and return filename. Worker will process later.
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")
    # In Step 2 we'll save file to object store / local folder and push to Celery.
    return {"filename": file.filename, "status": "accepted"}
