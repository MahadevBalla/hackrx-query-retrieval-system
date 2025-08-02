# app/llm.py

import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path="app/.env")

# It's better to use a more recent and capable model if available, but let's stick to the one you have for now.
# Note: "gemini-2.0-flash" is not a valid model name. A common one is "gemini-1.5-flash-latest". I'll use that.
API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"


def generate_answers(question: str, context_chunks: list[str]) -> str:
    # A more refined prompt focused on summarization and conciseness
    prompt = f"""
You are an expert AI assistant who creates concise summaries to answer questions about an insurance policy.
Your answers must be based *only* on the provided "Document Snippets".

Instructions:
1.  Carefully read the "Question" and the "Document Snippets".
2.  Synthesize the information to create a single, clear, and concise answer.
3.  Focus on the most important conditions and limits. Do not list every single exclusion unless it's critical to the question.
4.  If the question asks about a waiting period, find the specific duration (e.g., 24 months, 2 years).
5.  Your response should be a user-friendly summary, not a list of raw facts.
6.  If the answer absolutely cannot be found, respond with "The information required to answer this question is not available in the provided context."
7.  Respond in plain text without markdown or special symbols.

Document Snippets:
---
{"\n\n---\n".join(context_chunks)}
---

Question: {question}

Answer:
"""

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2, # Lower temperature for more factual answers
            "topP": 0.9,
            "topK": 40
        }
    }

    headers = {"Content-Type": "application/json", "X-goog-api-key": API_KEY}

    try:
        response = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        # Add a safety check for the response structure
        candidates = response.json().get("candidates", [])
        if candidates and "content" in candidates[0] and "parts" in candidates[0]["content"]:
            return candidates[0]["content"]["parts"][0]["text"].strip()
        else:
            return "Error: Received an unexpected response format from the API."
    except requests.exceptions.RequestException as e:
        return f"Error generating answer: A network error occurred. {str(e)}"
    except Exception as e:
        return f"Error generating answer: An unexpected error occurred. {str(e)}"