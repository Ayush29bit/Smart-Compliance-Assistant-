from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_and_embed(text: str, chunk_size=300):
    words = text.split()
    chunks = []
    current = []

    for word in words:
        current.append(word)
        if len(current) >= chunk_size:
            chunk_text = " ".join(current)
            embedding = model.encode(chunk_text).tolist()
            chunks.append((chunk_text, embedding))
            current = []

    if current:
        chunk_text = " ".join(current)
        embedding = model.encode(chunk_text).tolist()
        chunks.append((chunk_text, embedding))

    return chunks
