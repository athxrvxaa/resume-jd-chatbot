from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(
    title="Resume–JD Matching API",
    description="AI-powered resume and job description matching system",
    version="1.0.0"
)

app.include_router(router)
