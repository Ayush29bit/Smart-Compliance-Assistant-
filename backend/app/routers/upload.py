from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
from app.services.ocr import extract_text
from app.services.embedder import embed_document, store_vectors

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class UploadResponse(BaseModel):
    filename: str
    status: str


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(status_code=400, detail="No file uploaded")

    # 1. Save file to disk
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2. Extract text via OCR
    extracted_text = extract_text(file_path)

    # 3. Chunk + embed
    vectors = embed_document(extracted_text)

    # 4. Store embeddings in Qdrant
    store_vectors(vectors)

    return {"filename": file.filename, "status": "processed"}
