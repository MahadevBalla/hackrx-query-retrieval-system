import faiss
import numpy as np
from app.embedder import model

index = faiss.IndexFlatL2(384)


def retrieve_relevant_chunks(
    question: str, chunk_embeddings, chunks: list[str], top_k=5
):
    q_vec = model.encode([question])[0].reshape(1, -1).astype("float32")
    if not index.is_trained:
        index.add(chunk_embeddings.cpu().numpy().astype("float32"))
    D, I = index.search(q_vec, top_k)
    return [chunks[i] for i in I[0]]
