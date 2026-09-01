from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.ingester import extract_text_from_pdf
from src.parser import extract_contact_info, extract_skills
from src.scorer import calculate_text_similarity, compute_fit_score
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI(title = "Resume Parser API")

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],

)

@app.post("/api/screen")
async def screen_resume(
    resume: UploadFile = File( ... ),
    job_description :str = Form(...)
):

    if not resume.filename.endswith(".pdf"):
        raise HTTPException(status_code = 400, detail = "Only PDF files allowed.")

    # extract row text from pdf
    resume_text = extract_text_from_pdf(resume.file)

    # extract contact info and skills
    contacts = extract_contact_info(resume_text)
    candidate_skills = extract_skills(resume_text)
    jd_skills = extract_skills(job_description)

    # vector similarity(scorer.py function call)
    text_sim = calculate_text_similarity(resume_text, job_description)

    # final calculation
    results = compute_fit_score(candidate_skills, jd_skills, text_sim)
    results["contact_info"] = contacts
    return results
