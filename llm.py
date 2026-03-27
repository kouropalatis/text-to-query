"""
LLM client for the CampusAI API (OpenAI-compatible).
Credentials are read from ~/.env or .env in the current directory.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(os.path.expanduser("~/.env"))
load_dotenv()

_client = None


def get_client() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=os.getenv("CAMPUSAI_API_KEY"),
            base_url=os.getenv("CAMPUSAI_API_URL", "https://chat.campusai.compute.dtu.dk/api/v1"),
            timeout=180.0,
        )
    return _client


def call_llm(prompt: str) -> str:
    """Send a prompt to the LLM and return the text response."""
    client = get_client()
    model = os.getenv("CAMPUSAI_MODEL", "Gemma 3 (Chat)")
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=512,
    )
    return response.choices[0].message.content.strip()
