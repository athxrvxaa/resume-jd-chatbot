import re
from typing import Dict, List


SECTION_HEADERS = {
    "objective": ["objective", "career objective"],
    "education": ["education", "academic background"],
    "experience": ["experience", "work experience", "professional experience"],
    "internships": ["internships", "internship"],
    "projects": ["projects", "project"],
    "skills": ["skills", "technical skills"],
    "certifications": ["certifications", "certification"],
    "achievements": ["achievements", "awards"],
    "workshops": ["workshops", "events"],
    "interests": ["interests", "hobbies"]
}


def normalize(text: str) -> str:
    return re.sub(r'[^a-z]', '', text.lower())


def detect_sections(text: str) -> Dict[str, str]:
    sections: Dict[str, List[str]] = {}
    current_section = None

    lines = text.split("\n")

    for line in lines:
        normalized_line = normalize(line)

        for section, aliases in SECTION_HEADERS.items():
            for alias in aliases:
                if normalize(alias) == normalized_line:
                    current_section = section
                    sections[current_section] = []
                    break

        if current_section and normalized_line:
            sections[current_section].append(line)

    return {k: "\n".join(v) for k, v in sections.items()}
