"""
ATS Compatibility Diagnostic Engine.
Evaluates resume structure compliance, bullet quality, keyword density,
section hierarchy, and generates high-impact, prioritized fix recommendations.
"""

import re
from typing import List, Dict, Any, Optional

STANDARD_SECTIONS = {
    "summary": {
        "aliases": ["summary", "professional summary", "objective", "profile", "about me", "career objective"],
        "weight": 10,
        "required": False,
    },
    "experience": {
        "aliases": ["experience", "work experience", "professional experience", "employment", "employment history", "work history"],
        "weight": 25,
        "required": True,
    },
    "education": {
        "aliases": ["education", "academic background", "qualifications", "academic qualifications"],
        "weight": 15,
        "required": True,
    },
    "skills": {
        "aliases": ["skills", "technical skills", "core competencies", "competencies", "technologies", "tech stack", "expertise"],
        "weight": 20,
        "required": True,
    },
    "projects": {
        "aliases": ["projects", "personal projects", "key projects", "notable projects", "portfolio"],
        "weight": 15,
        "required": False,
    },
    "certifications": {
        "aliases": ["certifications", "certificates", "professional certifications", "licenses"],
        "weight": 5,
        "required": False,
    },
    "contact": {
        "aliases": [],
        "weight": 10,
        "required": True,
    },
}

STRONG_ACTION_VERBS = [
    "architected", "engineered", "designed", "developed", "built", "created",
    "implemented", "deployed", "launched", "spearheaded", "led", "managed",
    "optimized", "improved", "reduced", "increased", "scaled", "accelerated",
    "automated", "streamlined", "integrated", "delivered", "established",
    "pioneered", "transformed", "revamped", "mentored", "collaborated",
    "researched", "analyzed", "evaluated", "migrated", "refactored",
]

WEAK_VERBS = [
    "helped", "assisted", "worked on", "worked with", "was responsible for",
    "responsible for", "involved in", "participated in", "contributed to",
]

FORMATTING_RED_FLAGS = [
    (r"[^\x00-\x7F]+", "Non-ASCII / special characters detected"),
]


class ATSEngine:
    """Runs multi-dimensional ATS compliance checks against a resume text."""

    def run_diagnostics(
        self,
        resume_text: str,
        contact_info: Optional[Dict] = None,
        candidate_skills: Optional[List[Dict]] = None,
        jd_text: str = "",
    ) -> Dict[str, Any]:
        text_lower = resume_text.lower()
        word_count = len(resume_text.split())
        checks = []

        contact_score, contact_issues = self._check_contact(resume_text, contact_info)
        checks.append({"id": "contact_info", "label": "Contact Information", "score": contact_score, "max_score": 15, "status": self._status(contact_score, 15), "issues": contact_issues, "fix": "Include full name, professional email, phone number, city/state, and LinkedIn URL in the header."})

        section_score, found_sections, missing_sections = self._check_sections(text_lower)
        checks.append({"id": "section_headers", "label": "Standard Section Headers", "score": section_score, "max_score": 20, "status": self._status(section_score, 20), "issues": [f"Missing: {s.title()}" for s in missing_sections], "fix": f"Add standard headings. ATS bots rely on exact heading names.", "found_sections": found_sections, "missing_sections": missing_sections})

        quant_score, quant_issues = self._check_quantification(resume_text)
        checks.append({"id": "quantification", "label": "Quantified Achievements (X-Y-Z Formula)", "score": quant_score, "max_score": 20, "status": self._status(quant_score, 20), "issues": quant_issues, "fix": "Rewrite bullets: 'Accomplished [X] as measured by [Y] by doing [Z]'. E.g. 'Reduced API latency by 40% for 10k daily users by implementing Redis caching.'"})

        verb_score, verb_issues = self._check_action_verbs(resume_text)
        checks.append({"id": "action_verbs", "label": "Strong Action Verbs", "score": verb_score, "max_score": 15, "status": self._status(verb_score, 15), "issues": verb_issues, "fix": f"Lead bullets with strong engineering verbs: {', '.join(STRONG_ACTION_VERBS[:6])}."})

        keyword_score, keyword_issues = self._check_keyword_density(text_lower, jd_text.lower(), candidate_skills or [])
        checks.append({"id": "keyword_density", "label": "Job Description Keyword Alignment", "score": keyword_score, "max_score": 15, "status": self._status(keyword_score, 15), "issues": keyword_issues, "fix": "Mirror exact keywords from the job description in your Skills and Experience sections."})

        length_score, length_issues = self._check_length(word_count)
        checks.append({"id": "resume_length", "label": "Resume Length & Content Density", "score": length_score, "max_score": 10, "status": self._status(length_score, 10), "issues": length_issues, "fix": "Aim for 400-700 words for entry-level, up to 1000 for senior roles."})

        fmt_score, fmt_issues = self._check_formatting(resume_text)
        checks.append({"id": "formatting", "label": "ATS Formatting Compliance", "score": fmt_score, "max_score": 5, "status": self._status(fmt_score, 5), "issues": fmt_issues, "fix": "Use plain single-column text. Avoid tables, images, headers/footers, and special Unicode characters."})

        total_score = sum(c["score"] for c in checks)
        max_possible = sum(c["max_score"] for c in checks)
        ats_percentage = round((total_score / max_possible) * 100, 1)

        return {
            "overall_score": ats_percentage,
            "total_points": total_score,
            "max_points": max_possible,
            "grade": self._grade(ats_percentage),
            "checks": checks,
            "priority_fixes": self._prioritize_fixes(checks),
            "word_count": word_count,
            "found_sections": found_sections,
        }

    def _check_contact(self, text: str, contact_info: Optional[Dict]) -> tuple:
        score = 0
        issues = []
        if bool(re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)):
            score += 4
        else:
            issues.append("Professional email address missing")
        if bool(re.search(r"[\+\(]?\d[\d\s\-\(\)]{7,}\d", text)):
            score += 4
        else:
            issues.append("Phone number missing or undetectable")
        if bool(re.search(r"^[A-Z][a-z]+ [A-Z][a-z]+", text, re.M)) or (contact_info and contact_info.get("name")):
            score += 3
        else:
            issues.append("Full name not prominently detected at resume top")
        if bool(re.search(r"linkedin\.com/in/", text, re.I)):
            score += 2
        else:
            issues.append("LinkedIn profile URL missing")
        if bool(re.search(r"github\.com/", text, re.I)):
            score += 2
        else:
            issues.append("GitHub profile URL missing (recommended for tech roles)")
        return min(score, 15), issues

    def _check_sections(self, text_lower: str) -> tuple:
        found = []
        missing = []
        for section, config in STANDARD_SECTIONS.items():
            if section == "contact":
                continue
            if any(alias in text_lower for alias in config["aliases"]):
                found.append(section)
            elif config["required"]:
                missing.append(section)
        score = sum(5 if STANDARD_SECTIONS[s]["required"] else 3 for s in found)
        return min(score, 20), found, missing

    def _check_quantification(self, text: str) -> tuple:
        issues = []
        pct_count = len(re.findall(r"\d+\s*%", text))
        xyz_count = len(re.findall(r"(increased|decreased|reduced|improved|grew|achieved|delivered|saved|generated).{0,60}\d+", text, re.I))
        bullet_count = max(1, text.count("*") + text.count("-") + text.count("•"))
        density = (pct_count + xyz_count * 2) / bullet_count
        if pct_count == 0:
            issues.append("No percentage-based metrics found")
        if xyz_count == 0:
            issues.append("No result-oriented impact statements found")
        if density >= 0.5:
            score = 20
        elif density >= 0.3:
            score = 15
        elif density >= 0.1:
            score = 8
        else:
            score = 2
        return score, issues

    def _check_action_verbs(self, text: str) -> tuple:
        text_lower = text.lower()
        strong_found = [v for v in STRONG_ACTION_VERBS if v in text_lower]
        weak_found = [v for v in WEAK_VERBS if v in text_lower]
        issues = []
        if weak_found:
            issues.append(f"Weak verbs detected: {', '.join(weak_found[:3])}")
        if len(strong_found) < 3:
            issues.append(f"Only {len(strong_found)} strong action verb(s) found - aim for 6+")
        score = max(0, min(15, len(strong_found) * 2) - (len(weak_found) * 2))
        return score, issues

    def _check_keyword_density(self, text_lower: str, jd_lower: str, candidate_skills: List[Dict]) -> tuple:
        if not jd_lower.strip():
            return 10, ["No JD provided for keyword analysis"]
        stop = {"with", "that", "this", "from", "they", "will", "have", "been", "were", "your", "our", "their", "about"}
        jd_words = set(w for w in re.findall(r"\b[a-z]{4,}\b", jd_lower) if w not in stop)
        matches = sum(1 for w in jd_words if w in text_lower)
        coverage = matches / max(1, len(jd_words))
        issues = []
        if coverage < 0.3:
            issues.append(f"Low keyword overlap ({round(coverage*100)}%) with JD")
        elif coverage < 0.5:
            issues.append("Moderate keyword overlap - increase alignment with JD vocabulary")
        return min(15, round(coverage * 20)), issues

    def _check_length(self, word_count: int) -> tuple:
        issues = []
        if word_count < 200:
            issues.append(f"Resume is very short ({word_count} words)")
            return 2, issues
        elif word_count < 350:
            issues.append(f"Resume may be too brief ({word_count} words) - target 400-700")
            return 6, issues
        elif word_count <= 800:
            return 10, issues
        elif word_count <= 1100:
            issues.append(f"Resume is long ({word_count} words) - consider trimming")
            return 8, issues
        else:
            issues.append(f"Resume is very long ({word_count} words) - ATS may truncate")
            return 4, issues

    def _check_formatting(self, text: str) -> tuple:
        issues = []
        score = 5
        for pattern, msg in FORMATTING_RED_FLAGS:
            if re.search(pattern, text):
                issues.append(msg)
                score -= 2
        return max(0, score), issues

    @staticmethod
    def _status(score: int, max_score: int) -> str:
        ratio = score / max_score
        if ratio >= 0.85:
            return "PASS"
        elif ratio >= 0.55:
            return "WARN"
        return "FAIL"

    @staticmethod
    def _grade(pct: float) -> str:
        if pct >= 90: return "A+"
        elif pct >= 80: return "A"
        elif pct >= 70: return "B"
        elif pct >= 60: return "C"
        elif pct >= 50: return "D"
        return "F"

    @staticmethod
    def _prioritize_fixes(checks: List[Dict]) -> List[Dict]:
        failing = sorted([c for c in checks if c["status"] in ("FAIL", "WARN")], key=lambda c: c["max_score"] - c["score"], reverse=True)
        return [{"priority": i+1, "id": c["id"], "label": c["label"], "impact": f"+{c['max_score']-c['score']} pts", "fix": c["fix"]} for i, c in enumerate(failing[:3])]
