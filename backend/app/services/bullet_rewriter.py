import requests
from typing import List

OLLAMA_URL = "http://localhost:11434/api/generate"


SYSTEM_PROMPT = """
You are an expert resume writer.

STRICT RULES:
- Rewrite ONLY the provided bullets.
- DO NOT add new skills, tools, or experience.
- Do NOT invent metrics.
- Focus on clarity, impact, and alignment with the job description.
- Output bullet points only.
"""


def rewrite_bullets(
    bullets: List[str],
    jd_text: str,
    model: str = "llama3"
) -> List[str]:

    prompt = f"""
{SYSTEM_PROMPT}

Job Description:
{jd_text}

Original Resume Bullets:
{bullets}

Rewrite the bullets to better match the job description:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    rewritten = response.json()["response"].strip()

    return [line.strip("- ").strip() for line in rewritten.split("\n") if line.strip()]
