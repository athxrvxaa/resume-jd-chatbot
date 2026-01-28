from app.utils.pdf_reader import extract_text_from_pdf
from app.utils.text_cleaner import clean_text
from app.services.resume_parser import detect_sections
from app.services.skill_extractor import extract_skills_from_text
from app.services.jd_parser import extract_skills_from_jd
from app.services.similarity import skill_gap_analysis
from app.services.semantic_matcher import semantic_match
from app.services.final_matcher import final_match_score


if __name__ == "__main__":
    resume_path = "app/data/sample_resumes/resume.pdf"

    jd_text = """
    We are looking for a Machine Learning Engineer with strong Python skills.
    Experience with NLP, TensorFlow, PyTorch, SQL, and Docker is required.
    Experience with large-scale data processing is a plus.
    """

    raw = extract_text_from_pdf(resume_path)
    clean = clean_text(raw)
    sections = detect_sections(clean)

    resume_skills = set()
    resume_sentences = []

    for sec in ["skills", "projects", "experience", "internships"]:
        if sec in sections:
            resume_skills |= extract_skills_from_text(sections[sec])
            resume_sentences.extend(sections[sec].split("\n"))

    jd_skills = extract_skills_from_jd(jd_text)
    jd_sentences = jd_text.split("\n")

    rule_result = skill_gap_analysis(resume_skills, jd_skills)
    semantic_result = semantic_match(resume_sentences, jd_sentences)

    final_result = final_match_score(rule_result, semantic_result)

    print(final_result)
