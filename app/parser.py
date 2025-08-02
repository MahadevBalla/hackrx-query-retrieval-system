# app/parser.py

import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter

def parse_documents(path: str) -> list[str]:
    """
    Parses a PDF document, extracts text, and splits it into semantic chunks.
    """
    doc = fitz.open(path)
    full_text = ""
    for page in doc:
        full_text += page.get_text("text")
    doc.close()

    # Use a more sophisticated text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Larger chunk size to hold more context
        chunk_overlap=200, # Overlap to prevent losing context between chunks
        length_function=len,
    )
    
    chunks = text_splitter.split_text(full_text)
    return chunks