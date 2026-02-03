# 📄 Resume–JD Analysis & Chatbot (Local + Gemini LLM)

## Overview

This project is an **end-to-end AI resume analysis, rewriting, and chat system** that compares a candidate’s resume against a job description and provides:

- explainable match scores  
- missing skill analysis  
- actionable improvement suggestions  
- **LLM-powered resume bullet rewriting**  
- an interactive **chatbot with memory and streaming responses**

The system combines **deterministic NLP pipelines**, **semantic embeddings**, and **LLM reasoning** (local and cloud) inside a **Streamlit UI**.

It is designed to be **grounded, explainable, and provider-agnostic** — not a generic chatbot wrapper.

---

## Key Features

### 🔍 Resume–JD Matching

- Parses resume PDFs
- Cleans and segments text into logical sections
- Extracts skills from resume and job description
- Computes:
  - Rule-based skill match score
  - Semantic similarity score using sentence embeddings
- Produces an **explainable final match score**

---

### 🧠 Grounded Chatbot (Local + Gemini LLM)

- Supports **two LLM backends**:
  - **Local LLM** via Ollama (LLaMA 3)
  - **Gemini 2.5 Flash** (optional cloud backend)
- LLM is used **only for reasoning and rewriting**
- Resume parsing and scoring remain deterministic
- No hallucinated skills or experience
- Maintains **multi-turn conversational memory**
- Responses stream **word-by-word (ChatGPT-style)**

---

### ✨ Resume Bullet Rewriting

- Extracts bullets from resume sections (**Projects / Experience**)
- Allows **selective rewriting** of chosen bullets
- Rewrites are:
  - Job-description aware
  - Fact-preserving
  - Resume-ready
- Output is **editable and copy-friendly**

---

### 🖥️ Interactive UI (Streamlit)

- Upload resume PDF
- Paste job description
- View:
  - match scores
  - matched & missing skills
- Chat with the assistant in a **ChatGPT-style interface**
- Streamed responses (token-by-token)
- Sidebar-based bullet selection and rewriting
- LLM backend toggle (Local ↔ Gemini)

---

## System Architecture

- Resume PDF + Job Description  
          ↓
- Text Cleaning & Section Detection  
          ↓
- Skill Extraction (Rule-based)  
          ↓
- Semantic Matching (Embeddings)  
          ↓
- Final Explainable Scores  
          ↓
- Actionable Improvement Engine  
          ↓
- Local LLM Reasoning (Ollama)  
          ↓
- Streamlit Chat UI with Memory




---

## Tech Stack

- **Python**
- **Streamlit** – UI & chat interface
- **Sentence Transformers** – semantic embeddings
- **Ollama (LLaMA 3)** – local LLM inference
- **Gemini 2.5 Flash** – optional cloud LLM
- **PyMuPDF** – PDF parsing
- **Regex / Rule-based NLP** – skill extraction
- **Torch** – embedding similarity

✅ Works fully offline with local LLM  
✅ Cloud LLM is optional, not required  

---

## Why This Project Is Different

- Not a “ChatGPT wrapper”
- LLM does **not** parse resumes or invent experience
- All decisions are grounded in **deterministic NLP outputs**
- Provider-agnostic LLM design (local + cloud)
- Streaming responses improve UX without sacrificing control

### Real-world engineering challenges handled

- Python packaging & imports
- Circular dependency resolution
- Multi-entry-point execution (tests, Streamlit)
- Backend / frontend separation
- LLM provider abstraction

---

## How to Run Locally

### Prerequisites

- Python **3.10+**
- **Ollama** installed  
  👉 https://ollama.com  

---

### Run with Local LLM (Recommended)

Pull the model:
```bash
ollama pull llama3
```
Start Ollama (once):
```bash
ollama run llama3
```
Install Dependencies
```bash
pip install -r requirements.txt
```
Run the App

From project root:
```bash
streamlit run frontend/app.py
```

Then open:
```bash
http://localhost:8501
```
(Optional) Enable Gemini LLM
Set your API key
```bash
export GEMINI_API_KEY=your_key_here
```


## Example Use Cases
- Understand why a resume is rejected for a role
- Identify which skills matter most for a JD
- Improve resume bullets for ML / NLP roles
- Compare alignment across different job descriptions
- Get actionable, non-generic resume advice
- Rewrite resume bullets safely for a target role

## Project Structure
```bash
resume-jd-chatbot/
├── backend/
│   └── app/
│       ├── utils/        # PDF parsing, text cleaning
│       ├── services/     # NLP, matching, chatbot logic
│       └── models/       # Embeddings
├── frontend/
│   └── app.py            # Streamlit UI
└── tests/                # Pipeline & chatbot tests
```
---

## Future Improvements
- Intent routing (explain vs rewrite vs compare)
- Resume version comparison
- Long-term user memory
- Deployment (Docker / cloud)
- Evaluation dataset for scoring calibration

---

## Disclaimer

- This tool provides assistance, not guarantees.
- All resume rewrites preserve original content and should be reviewed before use.
- Users should review outputs before final submission.
---
