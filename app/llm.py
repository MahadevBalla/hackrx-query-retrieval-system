import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="app/.env")

API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def generate_answers(question: str, context_chunks: list[str]) -> str:
    prompt = f"Answer the question based on the context below:\n\nContext:\n{''.join(context_chunks)}\n\nQuestion: {question}"

    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    headers = {"Content-Type": "application/json", "X-goog-api-key": API_KEY}

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return f"Error generating answer: {str(e)}"
