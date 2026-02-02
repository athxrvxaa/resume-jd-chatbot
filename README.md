# 📄 Resume–JD Analysis & Chatbot (Local LLM)

## Overview

This project is an **end-to-end AI resume analysis and rewriting system** that compares a candidate’s resume against a job description and provides:

- Explainable match scores  
- Missing skill analysis  
- Actionable improvement suggestions  
- LLM-powered resume bullet rewriting  
- An interactive chatbot with memory  

The system combines **deterministic NLP techniques** with **semantic embeddings** and a **local LLM (no paid APIs)**, exposed through a **Streamlit UI**.

---

## Key Features

### 🔍 Resume–JD Matching

- Parses resume PDFs  
- Extracts skills from resume and job description  
- Computes:
  - Rule-based skill match score  
  - Semantic similarity score using sentence embeddings  
- Produces an **explainable final match score**

---

### 🧠 Grounded Chatbot (Local LLM)

- Uses a **local LLM via Ollama (LLaMA 3)**
- Answers questions like:
  - *Why is my resume not a perfect match?*
  - *What should I improve first?*
- Responses are grounded in structured NLP outputs  
- No hallucinated skills or experience  
- Maintains **multi-turn conversation memory**

---

### ✨ Resume Bullet Rewriting

- Extracts bullets from resume sections (**Projects / Experience**)  
- Allows selective rewriting of chosen bullets  
- Rewrites are:
  - Job-description aware  
  - Fact-preserving  
  - Resume-ready  
- Output is editable and copy-friendly  

---

### 🖥️ Interactive UI (Streamlit)

- Upload resume PDF  
- Paste job description  
- View scores and skill gaps  
- Chat with the assistant  
- Rewrite selected bullets via sidebar controls  

---

## System Architecture

Resume PDF + Job Description
↓
Text Cleaning & Section Detection
↓
Skill Extraction (Rule-based)
↓
Semantic Matching (Embeddings)
↓
Final Explainable Scores
↓
Actionable Improvement Engine
↓
Local LLM Reasoning (Ollama)
↓
Streamlit Chat UI with Memory

---

## Tech Stack

- **Python**
- **Streamlit** – UI  
- **Sentence Transformers** – semantic embeddings  
- **Ollama (LLaMA 3)** – local LLM inference  
- **PyMuPDF** – PDF parsing  
- **Regex / Rule-based NLP** – skill extraction  
- **Torch** – embedding similarity  

✅ No paid APIs  
✅ No cloud dependency  

---

## Why This Project Is Different

- Not a “ChatGPT wrapper”  
- LLM does **not** parse resumes or invent facts  
- All intelligence is grounded in deterministic NLP outputs  
- Designed with **explainability and control** in mind  

### Real-world engineering challenges handled:
- Python packaging  
- Circular imports  
- Multi-entry-point execution  
- Backend / frontend separation  

---

## How to Run Locally

### Prerequisites

- Python **3.10+**
- **Ollama** installed  
  👉 https://ollama.com  

Pull the model:

```bash
ollama pull llama3

Start Ollama (once):

ollama run llama3

Install Dependencies
pip install -r requirements.txt

Run the App

From project root:

streamlit run frontend/app.py


Then open:

http://localhost:8501

Example Use Cases

Understand why a resume is rejected for a role

Identify which skills matter most for a JD

Improve resume bullets for ML / NLP roles

Compare alignment across different job descriptions

Get actionable, non-generic resume advice

Project Structure
resume-jd-chatbot/
├── backend/
│   └── app/
│       ├── utils/        # PDF parsing, text cleaning
│       ├── services/     # NLP, matching, chatbot logic
│       └── models/       # Embeddings
├── frontend/
│   └── app.py            # Streamlit UI
└── tests/                # Pipeline & chatbot tests

Future Improvements

Intent routing (explain vs rewrite vs compare)

Resume version comparison

Long-term user memory

Deployment (Docker / cloud)

Evaluation dataset for scoring calibration

Disclaimer

This tool provides assistance, not guarantees.
All resume rewrites preserve original content and should be reviewed before use.

Author

Built as a learning-focused, end-to-end NLP & LLM system to demonstrate:

Applied NLP

Semantic similarity

Controlled LLM usage

Full-stack AI system design


---

If you want, next I can:
- tighten this for **GitHub recruiters**
- add **badges + demo GIF section**
- rewrite it for **LinkedIn project post**

Just tell me 👍
