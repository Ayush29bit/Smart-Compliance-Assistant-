# Smart-Compliance-Assistant-

📄 Smart Compliance Assistant — RAG Document Intelligence System
🚀 Overview

The Smart Compliance Assistant is an end-to-end AI-powered Document Intelligence system that can:

Read & extract text from PDFs, scanned images, and documents using OCR

Convert documents into meaningful vector embeddings

Store embeddings inside Qdrant (vector database)

Answer user questions through a custom RAG pipeline

Ground all answers strictly in the uploaded document

This project demonstrates real-world applied AI: combining OCR, vector databases, embeddings, and LLMs inside a modular backend architecture.

🧠 Features
✅ OCR Text Extraction

Uses EasyOCR / PDF utilities to convert both image-based and text-based PDFs into clean text.

✅ Chunking & Embedding

Breaks extracted text into readable chunks and embeds them using SentenceTransformer (all-MiniLM-L6-v2).

✅ Vector Storage (Qdrant)

Stores embeddings + text in Qdrant for fast semantic search.

✅ Retrieval-Augmented Generation (RAG)

For each user query:

Embed question

Retrieve most relevant chunks from Qdrant

Send them with the query to OpenAI GPT-4o-mini

Model responds only based on retrieved context

✅ Modular FastAPI Backend

API routes:

/upload → Upload & process documents

/query → Ask questions

/health → Service status

Each component is isolated into its own service layer for clean architecture.
