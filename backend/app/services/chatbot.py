import requests
from typing import Dict

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are an AI career assistant.

STRICT RULES:
- Use ONLY the provided analysis.
- DO NOT invent skills or experience.
- If something is missing, say so.
- Be concise, honest, and actionable.
"""


def build_context(analysis: Dict[str, object]) -> str:
    return f"""
MATCH SCORES:
- Final Score: {analysis['final_score']}
- Rule-based Score: {analysis['rule_score']}
- Semantic Score: {analysis['semantic_score']}

MATCHED SKILLS:
{analysis['matched_skills']}

MISSING SKILLS:
{analysis['missing_skills']}

SEMANTIC MATCHES:
{analysis['semantic_matches']}
"""


def chat_with_resume_bot(
    user_question: str,
    analysis: Dict[str, object],
    model: str = "llama3"
) -> str:

    prompt = f"""
{SYSTEM_PROMPT}

Here is the resume vs job description analysis:
{build_context(analysis)}

User question:
{user_question}

Answer:
"""

    print("\n=== DEBUG: PROMPT SENT TO LLM ===\n")
    print(prompt)

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    print("\n=== DEBUG: RAW RESPONSE ===\n")
    print(response.text)

    return response.json().get("response", "").strip()
