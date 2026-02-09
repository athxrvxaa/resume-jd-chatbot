from typing import List


def extract_bullets(text: str) -> List[str]:
    bullets = []
    current = ""

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        # if line looks like continuation, merge it
        if current and line[0].islower():
            current += " " + line
        else:
            if current:
                bullets.append(current)
            current = line

    if current:
        bullets.append(current)

    # keep only meaningful bullets
    return [b for b in bullets if len(b.split()) >= 6]
