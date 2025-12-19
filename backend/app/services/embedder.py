# app/services/embedder.py
import os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv

load_dotenv()

embedder = SentenceTransformer("all-MiniLM-L6-v2")

qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

COLLECTION_NAME = "documents"


def ensure_collection():
    collections = qdrant.get_collections().collections
    if COLLECTION_NAME not in [c.name for c in collections]:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(
                size=384,
                distance=models.Distance.COSINE
            )
        )


ensure_collection()


def embed_document(text: str):
    CHUNK_SIZE = 300
    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)
        if len(current) >= CHUNK_SIZE:
            chunk_text = " ".join(current)
            chunks.append({
                "text": chunk_text,
                "embedding": embedder.encode(chunk_text).tolist()
            })
            current = []

    if current:
        chunk_text = " ".join(current)
        chunks.append({
            "text": chunk_text,
            "embedding": embedder.encode(chunk_text).tolist()
        })

    return chunks

def embed_query(query: str):
    return embedder.encode(query).tolist()



def store_vectors(vectors):
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=i,
                vector=v["embedding"],
                payload={"text": v["text"]}
            )
            for i, v in enumerate(vectors)
        ]
    )
