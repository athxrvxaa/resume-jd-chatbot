from app.services.chatbot import chat_with_resume_bot

if __name__ == "__main__":

    # Mock analysis (THIS is important)
    analysis = {
        "final_score": 0.83,
        "rule_score": 0.71,
        "semantic_score": 1.0,
        "matched_skills": ["python", "machine learning", "nlp", "tensorflow", "sql"],
        "missing_skills": ["docker", "pytorch"],
        "semantic_matches": [
            {
                "jd_sentence": "Experience with NLP and large-scale data processing",
                "similarity": 0.53
            }
        ]
    }

    question = "Why is my resume not a perfect match for this job?"

    answer = chat_with_resume_bot(question, analysis)

    print("\nCHATBOT RESPONSE:\n")
    print(answer)
