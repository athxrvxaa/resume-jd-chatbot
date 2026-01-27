from app.utils.pdf_reader import extract_text_from_pdf
from app.utils.text_cleaner import clean_text

if __name__ == "__main__":
    pdf_path = r"E:\resume-jd-chatbot\backend\app\data\sample_resumes\resume.pdf"
    raw_text = extract_text_from_pdf(pdf_path)
    clean = clean_text(raw_text)

    print("--cleand text(first 1500 char)--")
    print(clean[:1500])