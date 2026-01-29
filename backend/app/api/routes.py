from fastapi import APIRouter, UploadFile, File, Form
import tempfile

from app.utils.pdf_reader import extract_text_from_pdf
from app.utils.text_cleaner import clean_text
from app.services.resume_parser import detect_sections
from app.services.skill_extractor import extract_skills_from_text
from app.services.jd_parser import extract_skills_from_jd
from app.services.similarity import skill_gap_analysis
from app.services.semantic_matcher import semantic_match
from app.services.final_matcher import final_match_score
from app.api.schemas import MatchResponse

router = APIRouter()


@router.post("/match", response_model=MatchResponse)
async def match_resume_jd(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await resume.read()
        tmp.write(content)
        tmp_path = tmp.name

    raw = extract_text_from_pdf(tmp_path)
    clean = clean_text(raw)
    sections = detect_sections(clean)

    resume_skills = set()
    resume_sentences = []

    for sec in ["skills", "projects", "experience", "internships"]:
        if sec in sections:
            resume_skills |= extract_skills_from_text(sections[sec])
            resume_sentences.extend(sections[sec].split("\n"))

    jd_skills = extract_skills_from_jd(job_description)
    jd_sentences = job_description.split("\n")

    rule_result = skill_gap_analysis(resume_skills, jd_skills)
    semantic_result = semantic_match(resume_sentences, jd_sentences)
    final_result = final_match_score(rule_result, semantic_result)

    return final_result
