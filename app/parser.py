import fitz


def parse_documents(path: str) -> list[str]:
    doc = fitz.open(path)
    full_text = ""
    for page in doc:
        full_text += page.get_text("text")
    chunks = [full_text[i : i + 500] for i in range(0, len(full_text), 500)]
    return chunks
