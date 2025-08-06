from sentence_transformers import SentenceTransformer
from fastapi import FastAPI

model = None
app = FastAPI()

@app.on_event("startup")
def load_model():
    global model
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_chunks(chunks: list[str]):
    return model.encode(chunks, convert_to_tensor=True)
