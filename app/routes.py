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

    file_path = download_file(req.documents)
    chunks = parse_documents(file_path)
    chunk_embeddings = embed_chunks(chunks)
    answers = []

    for q in req.questions:
        top_chunks = retrieve_relevant_chunks(q, chunk_embeddings, chunks)
        answer = generate_answers(q, top_chunks)
        answers.append(answer)

    return {"answers": answers}
