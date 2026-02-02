import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)



import streamlit as st

from backend.app.utils.pdf_reader import extract_text_from_pdf
from backend.app.utils.text_cleaner import clean_text
from backend.app.services.resume_parser import detect_sections
from backend.app.services.skill_extractor import extract_skills_from_text
from backend.app.services.jd_parser import extract_skills_from_jd
from backend.app.services.similarity import skill_gap_analysis
from backend.app.services.semantic_matcher import semantic_match
from backend.app.services.final_matcher import final_match_score
from backend.app.services.chatbot import chat_with_resume_bot
from backend.app.services.memory import ChatMemory




st.set_page_config(page_title="Resume Chatbot", layout="centered")
st.title("📄 Resume–JD Chatbot (Local LLM)")

st.write(
    "Upload your resume and job description. "
    "Then chat with an AI assistant that explains gaps and suggests improvements."
)

# ---------- SESSION STATE ----------
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "memory" not in st.session_state:
    st.session_state.memory = ChatMemory()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ---------- INPUTS ----------
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description", height=200)

# ---------- ANALYZE BUTTON ----------
if st.button("Analyze Resume"):
    if resume_file is None or not jd_text.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        with st.spinner("Analyzing resume..."):

            # Save uploaded PDF temporarily
            with open("temp_resume.pdf", "wb") as f:
                f.write(resume_file.read())

            # ---- PIPELINE ----
            raw = extract_text_from_pdf("temp_resume.pdf")
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
            analysis = final_match_score(rule_result, semantic_result)

            analysis["resume_sections_text"] = "\n".join(sections.values())
            analysis["jd_text"] = jd_text
            
            st.session_state.analysis = analysis
            st.session_state.memory = ChatMemory()
            st.session_state.chat_history = []

        st.success("Analysis complete!")

        st.subheader("📊 Match Summary")
        st.write(f"**Final Score:** {analysis['final_score']}")
        st.write(f"Rule-based Score: {analysis['rule_score']}")
        st.write(f"Semantic Score: {analysis['semantic_score']}")

        st.subheader("✅ Matched Skills")
        st.write(analysis["matched_skills"])

        st.subheader("❌ Missing Skills")
        st.write(analysis["missing_skills"])


# ---------- CHAT INTERFACE ----------
if st.session_state.analysis is not None:
    st.divider()
    st.subheader("💬 Chat with Resume Assistant")

    user_input = st.text_input("Ask a question about your resume:")

    if st.button("Send"):
        if user_input.strip():
            with st.spinner("Thinking..."):
                answer = chat_with_resume_bot(
                    user_input,
                    st.session_state.analysis,
                    st.session_state.memory
                )

            st.session_state.chat_history.append(
                {"user": user_input, "assistant": answer}
            )

    # Display chat history
    for turn in st.session_state.chat_history:
        st.markdown(f"**You:** {turn['user']}")
        st.markdown(f"**Assistant:** {turn['assistant']}")
