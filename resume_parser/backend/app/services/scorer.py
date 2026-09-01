"""
Upgraded Scoring Engine — Blueprint-compliant weighted formula:
Score = (Skills x 0.40) + (Experience x 0.25) + (Projects x 0.20) + (Education x 0.05) + (Semantic x 0.10)
"""

from typing import List, Dict, Any
from app.services.semantic_engine import SemanticEngine
import re


EDUCATION_KEYWORDS = {
    "phd": 100, "doctorate": 100, "ph.d": 100,
    "master": 80, "m.s.": 80, "m.sc": 80, "m.tech": 80, "mba": 80,
    "bachelor": 60, "b.s.": 60, "b.tech": 60, "b.e.": 60, "b.sc": 60,
    "associate": 40, "diploma": 30, "bootcamp": 20,
}


class ScorerService:
    """Computes blueprint-weighted candidate-JD fit with 3-tier skill matching."""

    def __init__(self):
        self.semantic_engine = SemanticEngine()

    def evaluate_candidate_fit(
        self,
        resume_text: str,
        jd_text: str,
        resume_skills: List[Dict[str, Any]],
        jd_skills: List[Dict[str, Any]],
        experience_years: float = 0.0,
        project_count: int = 0,
    ) -> Dict[str, Any]:
        """
        Blueprint-compliant scoring:
        Skills=40%, Experience=25%, Projects=20%, Education=5%, Semantic=10%
        """
        # ── 1. Semantic Similarity (used as one component) ─────────────────
        semantic_sim_pct = self.semantic_engine.compute_similarity(resume_text, jd_text)

        # ── 2. Skill Coverage — 3-tier match ──────────────────────────────
        resume_skill_map = {s["skill"].lower(): s for s in resume_skills}
        jd_skill_map = {s["skill"].lower(): s for s in jd_skills}

        exact_matches, semantic_matches, missing_skills = [], [], []

        for k, jd_s in jd_skill_map.items():
            if k in resume_skill_map:
                res_s = resume_skill_map[k]
                exact_matches.append({
                    "skill": jd_s["skill"],
                    "category": jd_s.get("category", "Technical"),
                    "match_type": "EXACT",
                    "confidence": 0.98,
                    "evidence": res_s.get("evidence", "Found in candidate resume."),
                })
            else:
                matched_sem = False
                for r_k, res_s in resume_skill_map.items():
                    if (jd_s.get("category") == res_s.get("category") and
                            jd_s.get("category") not in ("General", "Domain Specific / Discovered")):
                        semantic_matches.append({
                            "skill": jd_s["skill"],
                            "category": jd_s.get("category", "Technical"),
                            "match_type": "SEMANTIC",
                            "confidence": 0.80,
                            "evidence": f"Related to {res_s['skill']}: {res_s.get('evidence', '')}",
                        })
                        matched_sem = True
                        break
                if not matched_sem:
                    missing_skills.append({
                        "skill": jd_s["skill"],
                        "category": jd_s.get("category", "Technical"),
                        "match_type": "MISSING",
                        "confidence": 1.0,
                        "evidence": None,
                    })

        total_jd = len(jd_skill_map)
        if total_jd > 0:
            skill_score = (len(exact_matches) * 1.0 + len(semantic_matches) * 0.75) / total_jd
            skill_coverage_pct = round(min(1.0, skill_score) * 100, 2)
        else:
            skill_coverage_pct = 80.0 if resume_skills else 50.0

        # ── 3. Experience Score ────────────────────────────────────────────
        jd_exp_match = re.search(r"(\d+)\+?\s*(?:years?|yrs?)", jd_text, re.I)
        required_exp = float(jd_exp_match.group(1)) if jd_exp_match else 2.0
        if experience_years <= 0:
            experience_pct = 55.0  # neutral fallback if not extracted
        elif experience_years >= required_exp:
            experience_pct = min(100.0, 70.0 + (experience_years - required_exp) * 5)
        else:
            experience_pct = max(20.0, (experience_years / required_exp) * 70.0)

        # ── 4. Projects Score ──────────────────────────────────────────────
        projects_pct = min(100.0, project_count * 20.0) if project_count > 0 else 50.0

        # ── 5. Education Score ─────────────────────────────────────────────
        resume_lower = resume_text.lower()
        education_pct = 30.0  # baseline
        for keyword, score_val in EDUCATION_KEYWORDS.items():
            if keyword in resume_lower:
                education_pct = max(education_pct, float(score_val))
                break

        # ── 6. Blueprint Weighted Formula ──────────────────────────────────
        final_score = round(
            (skill_coverage_pct * 0.40) +
            (experience_pct * 0.25) +
            (projects_pct * 0.20) +
            (education_pct * 0.05) +
            (semantic_sim_pct * 0.10),
            2,
        )

        return {
            "final_score": final_score,
            "semantic_similarity": semantic_sim_pct,
            "skill_coverage": skill_coverage_pct,
            "experience_score": round(experience_pct, 2),
            "projects_score": round(projects_pct, 2),
            "education_score": round(education_pct, 2),
            "experience_years_detected": experience_years,
            "project_count_detected": project_count,
            "skills": {
                "matched": exact_matches + semantic_matches,
                "missing": missing_skills,
                "all_candidate_skills": resume_skills,
            },
        }
