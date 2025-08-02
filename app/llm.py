import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="app/.env")

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def generate_answers(question: str, context_chunks: list[str]) -> str:
    prompt = (
        "You are a helpful assistant answering policy-related questions using the provided document excerpts.\n"
        "Respond **only in plain text** without any Markdown, bullet points, or formatting symbols like '*', '**', or '-'.\n"
        # "Your answer should be factual, concise, and in complete sentences similar to an official policy summary.\n"
        "Avoid repeating phrases and do not speculate. Only answer if the information is clearly stated in the context.\n\n"
        "Document Snippets:\n"
        + "\n\n---\n".join(context_chunks)
        + f"\n\nQuestion: {question}\nAnswer:"
    )

    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    headers = {"Content-Type": "application/json", "X-goog-api-key": API_KEY}

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error generating answer: {str(e)}"
