from dotenv import load_dotenv
import os
from openai import OpenAI
from typing import Dict
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
You are an AI career assistant.

RULES (STRICT):
- You MUST use only the provided context.
- You MUST NOT invent skills, experience, or facts.
- If information is missing, say so clearly.
- Be concise, actionable, and honest.
- Explain reasoning step by step when appropriate.
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
    analysis: Dict[str, object]
) -> str:

    context = build_context(analysis)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""
Here is the resume vs JD analysis:

{context}

User question:
{user_question}
"""
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content
