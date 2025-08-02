# app/retriever.py

import faiss
import numpy as np
from .embedder import model # Use relative import for better package structure

def retrieve_relevant_chunks(
    question: str, index: faiss.Index, chunks: list[str], chunk_embeddings, top_k=5
):
    """
    Retrieves the most relevant chunks for a question from a pre-built FAISS index.
    """
    # Encode the question
    q_vec = model.encode([question], convert_to_tensor=False).astype("float32")
    
    # Search the index
    distances, indices = index.search(q_vec, top_k)
    
    # Return the corresponding chunks
    return [chunks[i] for i in indices[0]]