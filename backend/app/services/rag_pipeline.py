import os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http import models
import openai
from dotenv import load_dotenv

load_dotenv()

# ---------------------------
# 1. Load embedding model
# ---------------------------
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# ---------------------------
# 2. Connect to Qdrant
# ---------------------------
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL", "http://localhost:6333"),
    api_key=os.getenv("QDRANT_API_KEY")
)


COLLECTION_NAME = "documents"

# Create collection if not exists
def ensure_collection():
    collections = qdrant.get_collections().collections
    existing = [c.name for c in collections]
    if COLLECTION_NAME not in existing:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE)
        )

ensure_collection()


# ---------------------------
# 3. EMBEDDING FUNCTION
# ---------------------------
def embed_document(text: str):
    """
    Takes plain text, splits into chunks, embeds them.
    Returns list of dicts = [{"text": "...", "embedding": [...]}, ...]
    """
    chunks = []

    # Simple rule-based chunking
    CHUNK_SIZE = 300
    words = text.split()

    current = []
    for word in words:
        current.append(word)
        if len(current) >= CHUNK_SIZE:
            chunk_text = " ".join(current)
            embedding = embedder.encode(chunk_text).tolist()
            chunks.append({"text": chunk_text, "embedding": embedding})
            current = []

    # Last chunk
    if current:
        chunk_text = " ".join(current)
        embedding = embedder.encode(chunk_text).tolist()
        chunks.append({"text": chunk_text, "embedding": embedding})

    return chunks


# ---------------------------
# 4. STORE VECTORS IN QDRANT
# ---------------------------
def store_vectors(vectors: list):
    """
    Takes list like [{"text": "...", "embedding": [...]}, ...]
    Stores in Qdrant.
    """
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


# ---------------------------
# 5. RETRIEVE RELEVANT CHUNKS
# ---------------------------
def retrieve(query: str):
    """
    Search Qdrant for relevant chunks.
    """
    query_vec = embedder.encode(query).tolist()

    results = qdrant.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vec,
        limit=5
    )

    chunks = [hit.payload["text"] for hit in results]
    return chunks


# ---------------------------
# 6. GENERATE FINAL ANSWER (LLM)
# ---------------------------
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_answer(query, chunks):
    """
    Combines retrieved chunks & query → sends to LLM.
    """
    context = "\n\n".join(chunks)

    prompt = f"""
    You are a helpful assistant answering questions based on the given context.

    CONTEXT:
    {context}

    QUESTION:
    {query}

    Answer based ONLY on the context above.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]


# ---------------------------
# 7. MAIN RAG PIPELINE
# ---------------------------
def run_rag(query: str):
    """
    Full RAG: retrieve → LLM answer
    """
    chunks = retrieve(query)
    answer = generate_answer(query, chunks)
    return answer

