import pdfplumber


def parse_documents(path: str) -> list[str]:
    chunks = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                chunks.extend([text[i : i + 500] for i in range(0, len(text), 500)])
    return chunks
