from typing import List


def extract_bullets(text: str) -> List[str]:
    bullets = []

    for line in text.split("\n"):
        line = line.strip()
        if len(line.split()) >= 5:
            bullets.append(line)

    return bullets
