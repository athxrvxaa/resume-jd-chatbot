from app.utils.pdf_reader import extract_text_from_pdf
from app.utils.text_cleaner import clean_text
from app.services.resume_parser import detect_sections

if __name__ == "__main__":
    pdf_path = r"E:\resume-jd-chatbot\backend\app\data\sample_resumes\resume.pdf"

    raw = extract_text_from_pdf(pdf_path)
    clean = clean_text(raw)
    sections = detect_sections(clean)

    for section, content in sections.items():
        print(f"\n===== {section.upper()} =====")
        print(content[:500])
