import sys
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

import streamlit as st

from backend.app.services.skill_actions import skill_action
from backend.app.services.bullet_extractor import extract_bullets
from backend.app.services.bullet_rewriter import rewrite_bullets
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


# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Resume Chatbot", layout="centered")
st.title("📄 Resume–JD Chatbot (Local / Gemini)")

st.write(
    "Upload your resume and job description. "
    "Then chat with an AI assistant that explains gaps and suggests improvements."
)

# ---------- SIDEBAR: LLM SETTINGS ----------
st.sidebar.header("⚙️ LLM Settings")

llm_provider = st.sidebar.selectbox(
    "Choose LLM",
    ["local", "gemini"]
)

# ---------- SESSION STATE ----------
if "analysis" not in st.session_state:
    st.session_state.analysis = None

if "memory" not in st.session_state:
    st.session_state.memory = ChatMemory()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- INPUTS ----------
resume_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
jd_text = st.text_area("Paste Job Description", height=200)

# ---------- ANALYZE ----------
if st.button("Analyze Resume"):
    if resume_file is None or not jd_text.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        with st.spinner("Analyzing resume..."):

            with open("temp_resume.pdf", "wb") as f:
                f.write(resume_file.read())

            raw = extract_text_from_pdf("temp_resume.pdf")
            clean = clean_text(raw)
            sections = detect_sections(clean)

            # ---- EXTRACT BULLETS ----
            resume_bullets = {}
            for sec in ["projects", "experience"]:
                if sec in sections:
                    resume_bullets[sec] = extract_bullets(sections[sec])

            st.session_state.resume_bullets = resume_bullets

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
            st.session_state.messages = []

        st.success("Analysis complete!")

        st.subheader("📊 Match Summary")
        st.write(f"**Final Score:** {analysis['final_score']}")
        st.write(f"Rule-based Score: {analysis['rule_score']}")
        st.write(f"Semantic Score: {analysis['semantic_score']}")

        st.subheader("✅ Matched Skills")
        st.write(analysis["matched_skills"])

        st.subheader("❌ Missing Skills")
        st.write(analysis["missing_skills"])
        st.subheader("🛠️ How to Improve Missing Skills")

        for skill in st.session_state.analysis["missing_skills"]:
            st.markdown(f"**{skill.upper()}**")
            st.markdown(f"- {skill_action(skill)}")




# ---------- SIDEBAR: BULLET REWRITE ----------
if (
    st.session_state.analysis is not None
    and "resume_bullets" in st.session_state
):

    st.sidebar.divider()
    st.sidebar.header("✂️ Rewrite Resume Bullets")

    selected_section = st.sidebar.selectbox(
        "Select section",
        options=list(st.session_state.resume_bullets.keys())
    )

    selected_bullets = []

    if selected_section:
        st.sidebar.subheader("Select bullets")

        for i, bullet in enumerate(
            st.session_state.resume_bullets[selected_section]
        ):
            if st.sidebar.checkbox(
                bullet,
                key=f"{selected_section}_{i}"
            ):
                selected_bullets.append(bullet)

    if st.sidebar.button("Rewrite Selected Bullets"):
        if not selected_bullets:
            st.sidebar.warning("Select at least one bullet.")
        else:
            with st.sidebar.spinner("Rewriting bullets..."):
                rewritten = rewrite_bullets(
                    bullets=selected_bullets,
                    jd_text=st.session_state.analysis["jd_text"]
                )

            st.subheader("✨ Rewritten Bullets")
            st.text_area(
                "You can edit and copy these bullets:",
                value="\n".join([f"- {b}" for b in rewritten]),
                height=200
            )

# ---------- CHAT ----------
if st.session_state.analysis is not None:

    st.divider()
    st.subheader("💬 Resume Assistant")

    # display chat history (TOP → BOTTOM)
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # chat input
    if prompt := st.chat_input("Ask something about your resume"):
        # user message
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            streamed_text = ""

            response_stream = chat_with_resume_bot(
                prompt,
                st.session_state.analysis,
                st.session_state.memory,
                model=llm_provider,
                stream=True
            )

            for token in response_stream:
                streamed_text += token
                placeholder.markdown(streamed_text)

        st.session_state.messages.append(
            {"role": "assistant", "content": streamed_text}
        )
