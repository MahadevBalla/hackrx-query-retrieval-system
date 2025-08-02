# app/routes.py

import faiss
import numpy as np
from fastapi import APIRouter, Request, Header, HTTPException
from pydantic import BaseModel
from app.parser import parse_documents
from app.embedder import embed_chunks
from app.retriever import retrieve_relevant_chunks
from app.llm import generate_answers
from app.utils import download_file

router = APIRouter()


class QueryRequest(BaseModel):
    documents: str
    questions: list[str]


@router.post("/api/v1/hackrx/run")
async def handle_query(req: QueryRequest, authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")

    # 1. Download and Parse
    file_path = download_file(req.documents)
    chunks = parse_documents(file_path)

    # 2. Embed all chunks
    # Note: .cpu() is needed if embeddings were generated on a GPU
    chunk_embeddings = embed_chunks(chunks).cpu().numpy().astype("float32")

    # 3. Build the FAISS index ONCE
    embedding_dimension = chunk_embeddings.shape[1]
    index = faiss.IndexFlatL2(embedding_dimension)
    index.add(chunk_embeddings)

    # 4. Process all questions using the single index
    answers = []
    for q in req.questions:
        # Pass the existing index to the retriever
        top_chunks = retrieve_relevant_chunks(q, index, chunks, chunk_embeddings, top_k=7)
        answer = generate_answers(q, top_chunks)
        answers.append(answer)

    return {"answers": answers}