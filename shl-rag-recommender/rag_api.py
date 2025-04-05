# rag_api.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import pickle
import faiss
from sentence_transformers import SentenceTransformer
import numpy as np

# Load index + metadata
with open("data/shl_metadata.pkl", "rb") as f:
    metadata = pickle.load(f)

index = faiss.read_index("data/shl_index.faiss")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

app = FastAPI()

# Allow Streamlit or any client to access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RAGResponse(BaseModel):
    question: str
    results: List[dict]

@app.get("/ask", response_model=RAGResponse)
async def ask(query: str = Query(..., min_length=3), k: int = 5):
    query_embedding = embedder.encode([query])
    scores, indices = index.search(np.array(query_embedding), k)
    results = [metadata[i] for i in indices[0] if i < len(metadata)]

    return {"question": query, "results": results}
