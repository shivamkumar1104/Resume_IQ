"""FastAPI Main Server - Resume Intelligence Platform v3.0"""

import time
import os
from contextlib import asynccontextmanager
from pathlib import Path
import sys
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.services.ingester import extract_text, extract_text_from_pdf
from app.services.parser import extract_contact_info, extract_experience_years, count_projects
from app.services.skill_engine import UniversalSkillEngine
from app.services.semantic_engine import SemanticEngine
from app.services.scorer import ScorerService
from app.services.template_engine import TemplateEngine, COMPANY_TEMPLATES
from app.services.optimizer import ResumeOptimizer
from app.services.ats_engine import ATSEngine
from app.schemas.screening import ScreeningResult

# Initialize AI engines
skill_engine = UniversalSkillEngine()
semantic_engine = SemanticEngine()
scorer_service = ScorerService()
template_engine = TemplateEngine()
optimizer = ResumeOptimizer()
ats_engine = ATSEngine()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        semantic_engine.load_model()
    except Exception as e:
        print(f"Warning loading semantic engine: {e}")
    yield


app = FastAPI(
    title="Resume Intelligence Platform",
    description="Enterprise-grade AI candidate screening: universal skill intelligence, ATS diagnostics, explainable scoring, and company template engine.",
    version="3.0.0",
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan,
)

# Robust CORS configuration: allows all origins by default or specific comma-separated origins from ENV
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "*")
if allowed_origins_env.strip() == "*":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "Resume Intelligence Platform API",
        "version": "3.0.0",
        "health": "/api/health",
        "docs": "/api/docs",
    }


@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "Resume Intelligence Platform", "version": "3.0.0"}


@app.get("/api/templates")
def get_company_templates():
    return {"templates": COMPANY_TEMPLATES}


@app.post("/api/screen")
async def screen_candidate(
    resume: UploadFile = File(..., description="Candidate PDF or DOCX Resume"),
    job_description: str = Form(..., description="Target Job Description Text"),
):
    """
    Complete 6-Stage Screening Pipeline:
    1. Document Ingestion (PDF/DOCX)
    2. Contact & Name Extraction (SpaCy NER)
    3. Universal Skill Intelligence (3-tier: Exact / Semantic / Missing)
    4. Blueprint-Weighted Scoring: Skills(40%) + Exp(25%) + Projects(20%) + Edu(5%) + Semantic(10%)
    5. Full ATS Diagnostic Engine (7 checks)
    6. Grounded AI Improvement Suggestions + Template Recommendations
    """
    start_time = time.time()

    filename_lower = resume.filename.lower()
    if not (filename_lower.endswith(".pdf") or filename_lower.endswith(".docx")):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX resumes are supported.")

    if not job_description.strip():
        raise HTTPException(status_code=400, detail="Please provide a valid job description.")

    pdf_bytes = await resume.read()

    # 1. Text extraction
    try:
        resume_text = extract_text(pdf_bytes, resume.filename)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Failed to extract text from resume: {str(e)}")

    if not resume_text.strip():
        raise HTTPException(status_code=422, detail="Could not extract any text from resume. Ensure it is not a scanned image-only PDF.")

    # 2. Contact & structural metadata
    contacts = extract_contact_info(resume_text)
    exp_years = extract_experience_years(resume_text)
    project_count = count_projects(resume_text)

    # 3. Skill extraction
    candidate_skills = skill_engine.extract_skills_with_evidence(resume_text)
    jd_skills = skill_engine.extract_skills_with_evidence(job_description)

    # 4. Blueprint-weighted scoring
    evaluation = scorer_service.evaluate_candidate_fit(
        resume_text=resume_text,
        jd_text=job_description,
        resume_skills=candidate_skills,
        jd_skills=jd_skills,
        experience_years=exp_years,
        project_count=project_count,
    )

    # 5. ATS Diagnostics
    ats_report = ats_engine.run_diagnostics(
        resume_text=resume_text,
        contact_info=contacts,
        candidate_skills=candidate_skills,
        jd_text=job_description,
    )

    # 6a. AI Recommendations
    recommendations = optimizer.generate_recommendations(
        resume_text=resume_text,
        missing_skills=evaluation["skills"]["missing"],
        matched_skills=evaluation["skills"]["matched"],
    )

    # 6b. Template Recommendations
    matched_skill_names = [s["skill"] for s in candidate_skills]
    recommended_templates = template_engine.recommend_templates(
        jd_text=job_description,
        candidate_skills=matched_skill_names,
    )

    elapsed_ms = int((time.time() - start_time) * 1000)

    return {
        "filename": resume.filename,
        "contact": contacts,
        "scores": {
            "final_score": evaluation["final_score"],
            "semantic_similarity": evaluation["semantic_similarity"],
            "skill_coverage": evaluation["skill_coverage"],
            "experience_score": evaluation.get("experience_score", 0),
            "projects_score": evaluation.get("projects_score", 0),
            "education_score": evaluation.get("education_score", 0),
            "ats_score": ats_report["overall_score"],
            "experience_years_detected": evaluation.get("experience_years_detected", 0),
            "project_count_detected": evaluation.get("project_count_detected", 0),
        },
        "skills": evaluation["skills"],
        "ats_report": ats_report,
        "improvements": recommendations,
        "recommended_templates": recommended_templates,
        "processing_time_ms": elapsed_ms,
    }
