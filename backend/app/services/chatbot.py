import requests
from typing import Dict

from app.services.memory import ChatMemory
from app.services.improvement_engine import generate_improvements


OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are an AI career assistant.

STRICT RULES:
- Use ONLY the provided analysis.
- DO NOT invent skills, experience, or projects.
- If something is missing, say so clearly.
- Give actionable, practical advice.
- Be concise and professional.
"""


def build_context(analysis: Dict[str, object]) -> str:
    improvements = generate_improvements(analysis["missing_skills"])

    return f"""
MATCH SCORES:
- Final Score: {analysis['final_score']}
- Rule-based Score: {analysis['rule_score']}
- Semantic Score: {analysis['semantic_score']}

MATCHED SKILLS:
{analysis['matched_skills']}

MISSING SKILLS:
{analysis['missing_skills']}

ACTIONABLE IMPROVEMENTS:
{improvements}

SEMANTIC MATCHES:
{analysis['semantic_matches']}
"""


def chat_with_resume_bot(
    user_question: str,
    analysis: Dict[str, object],
    memory: ChatMemory,
    model: str = "llama3"
) -> str:

    conversation_history = memory.format_history()

    prompt = f"""
{SYSTEM_PROMPT}

Conversation so far:
{conversation_history}

Here is the resume vs job description analysis:
{build_context(analysis)}

User question:
{user_question}

Answer:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )

    answer = response.json()["response"].strip()

    memory.add_turn(user_question, answer)

    return answer
