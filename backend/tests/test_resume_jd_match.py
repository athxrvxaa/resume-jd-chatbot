from app.utils.pdf_reader import extract_text_from_pdf
from app.utils.text_cleaner import clean_text
from app.services.resume_parser import detect_sections
from app.services.skill_extractor import extract_skills_from_text
from app.services.jd_parser import extract_skills_from_jd
from app.services.similarity import skill_gap_analysis

if __name__ == "__main__":
    resume_path = "app/data/sample_resumes/resume.pdf"

    jd_text = """
    We are looking for a Machine Learning Engineer with strong Python skills.
    Experience with NLP, TensorFlow, PyTorch, SQL, and Docker is required.
    """

    raw = extract_text_from_pdf(resume_path)
    clean = clean_text(raw)
    sections = detect_sections(clean)

    resume_skills = set()
    for sec in ["skills", "projects", "experience", "internships"]:
        if sec in sections:
            resume_skills |= extract_skills_from_text(sections[sec])

    jd_skills = extract_skills_from_jd(jd_text)

    result = skill_gap_analysis(resume_skills, jd_skills)

    print(result)
