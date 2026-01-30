import streamlit as st
import requests

BACKEND_URL = "http://backend:8000/match"

st.set_page_config(page_title="Resume JD Matcher", layout="centered")

st.title("Resume–Job Description Matcher")
st.write("Upload your resume and paste the job description to see how well you match.")

resume_file = st.file_uploader("Upload Resume (PDF only)", type=["pdf"])

job_description = st.text_area(
    "Paste Job Description",
    height=200,
    placeholder="Enter the job description here..."
)

if st.button("Analyze"):
    if resume_file is None or not job_description.strip():
        st.warning("Please upload a resume and paste a job description.")
    else:
        with st.spinner("Analyzing resume..."):
            files = {
                "resume": (resume_file.name, resume_file, "application/pdf")
            }
            data = {
                "job_description": job_description
            }

            try:
                response = requests.post(BACKEND_URL, files=files, data=data)
                result = response.json()

                st.success("Analysis complete!")

            
                st.subheader("Match Scores")
                st.metric("Final Match Score", result["final_score"])
                col1, col2 = st.columns(2)
                col1.metric("Rule-based Score", result["rule_score"])
                col2.metric("Semantic Score", result["semantic_score"])

            
                st.subheader("Matched Skills")
                st.write(result["matched_skills"] or "None")

                st.subheader("Missing Skills")
                st.write(result["missing_skills"] or "None")

            
                if result["semantic_matches"]:
                    st.subheader("Semantic Matches")
                    for match in result["semantic_matches"]:
                        st.write(
                            f"- **JD Requirement:** {match['jd_sentence']} "
                            f"(similarity: {match['similarity']})"
                        )

            except Exception as e:
                st.error(f"Error connecting to backend: {e}")
