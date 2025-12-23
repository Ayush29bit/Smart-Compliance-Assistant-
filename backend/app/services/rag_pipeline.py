import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from groq import Groq
from dotenv import load_dotenv

from app.services.embedder import embed_document, embed_query

load_dotenv()

COLLECTION_NAME = "documents"

# Qdrant
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)

# Groq (free and fast!)
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ensure_collection():
    collections = [c.name for c in qdrant.get_collections().collections]
    if COLLECTION_NAME not in collections:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )

ensure_collection()

def store_vectors(vectors):
    """Store vectors in Qdrant"""
    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=i,
                vector=v["embedding"],
                payload={"text": v["text"]}
            )
            for i, v in enumerate(vectors)
        ]
    )

def retrieve_chunks(query: str, limit: int = 5):
    query_vector = embed_query(query)

    results = qdrant.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=limit
    )

    return [point.payload["text"] for point in results.points]

def generate_answer(query: str, chunks: list[str]):
    context = "\n\n".join(chunks)

    # Using Groq instead of OpenAI
    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",  # Free and powerful
        messages=[
            {
                "role": "system",
                "content": "Answer strictly using the provided context."
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion:\n{query}"
            }
        ],
        temperature=0.5,
        max_tokens=1024
    )

    return response.choices[0].message.content

def run_rag(query: str):
    chunks = retrieve_chunks(query)
    return generate_answer(query, chunks)
