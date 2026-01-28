from typing import Set
from app.services.skill_extractor import extract_skills_from_text

def extract_skills_from_jd(jd_text: str) -> Set[str]:
    return extract_skills_from_text(jd_text)