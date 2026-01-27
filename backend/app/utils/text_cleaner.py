import re

def clean_text(text: str) -> str:
    text = re.sub(r'[ \t]+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'[^\x20-\x7E\n]', '', text)
    lines = [line.strip() for line in text.split('\n')]
    lines = [line for line in lines if line]

    return '\n'.join(lines)