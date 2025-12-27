from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import os
from app.services.docling_service import extract_text
from app.services.embedder import embed_document, store_vectors

router = APIRouter()

UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class UploadResponse(BaseModel):
    filename: str
    status: str

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        print(f"Received file: {file.filename}")
        print(f"Content type: {file.content_type}")
        
        if not file:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # 1. Save file to disk
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        
        print(f"File saved to: {file_path}")

        # 2. Extract text via OCR
        extracted_text = extract_text(file_path)
        print(f"Extracted text length: {len(extracted_text)}")

        # 3. Chunk + embed
        vectors = embed_document(extracted_text)
        print(f"Generated {len(vectors)} vectors")

        # 4. Store embeddings in Qdrant
        store_vectors(vectors)
        print("Vectors stored successfully")

        return {"filename": file.filename, "status": "processed"}
    
    except Exception as e:
        print(f"Error in upload_file: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))