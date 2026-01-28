from typing import Set
import re

SKILL_KEYWORDS = {
    "python", "java", "c++", "sql", "javascript", "html", "css",
    "machine learning", "deep learning", "nlp",
    "tensorflow", "keras", "pytorch",
    "scikit-learn", "numpy", "pandas",
    "opencv", "pytesseract",
    "docker", "git", "linux",
    "fastapi", "flask"
}

def extract_skills_from_text(text: str) -> Set[str]:
    text = text.lower()
    found_skills = set()

    for skill in SKILL_KEYWORDS:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.add(skill)

    return found_skills