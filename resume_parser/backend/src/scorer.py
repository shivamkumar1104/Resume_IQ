from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_text_similarity(resume_text: str, jd_text: str)-> float:
    vectorizer =  TfidfVectorizer(stop_words = 'english', ngram_range = (1,2))
    tfidf_matrix = vectorizer.fit_transform([resume_text, jd_text])
    sim_matrix = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
    return float(sim_matrix[0][0])

def compute_fit_score(resume_skills: list, jd_skills: list, text_sim: float) -> dict:
    jd_skill_set = set([s.title() for s in jd_skills])
    resume_skill_set = set([s.title() for s in resume_skills])

    matched_skills = jd_skill_set.intersection(resume_skill_set)
    missing_skills = jd_skill_set.difference(resume_skill_set)

    skill_match_ratio = len(matched_skills) / len(jd_skill_set) if len(jd_skill_set) > 0 else 0.0

    final_score = round(((text_sim *0.5) + (skill_match_ratio * 0.5)) * 100, 2)

    return {
        "final_score": final_score,
        "text_similarity_pct": round(text_sim * 100,2),
        "skill_match_pct": round(skill_match_ratio *100, 2),
        "matched_skills": list(matched_skills),
        "missing_skills": list(missing_skills),

    }