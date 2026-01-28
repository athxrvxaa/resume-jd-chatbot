from app.services.semantic_matcher import semantic_match

if __name__ == "__main__":
    resume_sentences = [
        "Built Spark pipelines on AWS for large datasets",
        "Implemented NLP models using TensorFlow",
        "Developed OCR systems using Pytesseract"
    ]
    jd_sentences = [
        "Experience with large-scale data processing",
        "Strong background in Natural Language Processing",
        "Experience with Docker"
    ]

    result = semantic_match(resume_sentences , jd_sentences)
    print(result)