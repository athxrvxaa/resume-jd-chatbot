import os
import requests
from dotenv import load_dotenv
from pathlib import Path
from google import genai

# -------------------------------------------------
# Load environment variables EXPLICITLY
# -------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[3]
load_dotenv(dotenv_path=ROOT_DIR / ".env")

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
OLLAMA_URL = "http://localhost:11434/api/generate"
GEMINI_MODEL = "models/gemini-2.5-flash"

# -------------------------------------------------
# GEMINI CLIENT (fail fast)
# -------------------------------------------------
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY not found. "
        "Check .env path or environment variables."
    )

client = genai.Client(api_key=api_key)


# -------------------------------------------------
# PUBLIC API
# -------------------------------------------------
def generate_llm_response(
    prompt: str,
    provider: str = "local",
    stream: bool = False
):
    """
    provider: 'local' | 'gemini'
    """

    if provider == "local":
        return _ollama_generate(prompt, stream)

    elif provider == "gemini":
        return _gemini_generate(prompt, stream)

    else:
        raise ValueError("Unsupported LLM provider")


# -------------------------------------------------
# OLLAMA (LOCAL LLM)
# -------------------------------------------------
def _ollama_generate(prompt: str, stream: bool):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": stream
        },
        stream=stream
    )

    if not stream:
        return response.json()["response"]

    for line in response.iter_lines():
        if line:
            chunk = line.decode("utf-8")
            if '"response":"' in chunk:
                yield chunk.split('"response":"')[1].split('"')[0]


# -------------------------------------------------
# GEMINI (CLOUD LLM)
# -------------------------------------------------
def _gemini_generate(prompt: str, stream: bool):
    """
    NOTE:
    Gemini API does NOT support true token streaming like Ollama.
    If stream=True, we return a generator that yields once.
    """

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    if not stream:
        return response.text

    # pseudo-stream (single yield)
    yield response.text
