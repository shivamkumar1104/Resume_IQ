"""Grounded AI Resume Improvement & Recommendation Engine."""

from typing import List, Dict, Any


class ResumeOptimizer:
    """Generates actionable, grounded resume improvement recommendations."""

    def generate_recommendations(
        self,
        resume_text: str,
        missing_skills: List[Dict[str, Any]],
        matched_skills: List[Dict[str, Any]],
    ) -> List[Dict[str, str]]:
        """
        Generate grounded suggestions without fabricating candidate experience.
        """
        recommendations = []

        # 1. Critical Missing Skills Suggestion
        if missing_skills:
            top_missing = [s["skill"] for s in missing_skills[:3]]
            recommendations.append({
                "type": "CRITICAL_SKILL",
                "title": f"Target Role Keywords Missing ({', '.join(top_missing)})",
                "description": f"The job description highlights requirements for {', '.join(top_missing)}.",
                "suggestion": f"If you possess hands-on experience or academic projects using {top_missing[0]}, explicitly highlight it under your Technical Skills and Project sections."
            })

        # 2. Quantification / Metric Suggestion
        numbers_found = any(char.isdigit() for char in resume_text)
        if not numbers_found or resume_text.count("%") + sum(1 for w in resume_text.split() if w.replace(".", "").isdigit()) < 4:
            recommendations.append({
                "type": "QUANTIFICATION",
                "title": "Quantify Achievement Impact (Google X-Y-Z Formula)",
                "description": "Recruiters and ATS favor bullet points with measurable outcomes (e.g. latency reduced, users served, efficiency gained).",
                "suggestion": "Rewrite generic bullet points like 'Built API with FastAPI' to 'Architected 10+ REST endpoints with FastAPI, reducing response latency by 25% for 5k active users'."
            })

        # 3. Action Verb & Evidence Reinforcement
        strong_verbs = ["architected", "engineered", "optimized", "spearheaded", "deployed", "scaled"]
        verbs_present = sum(1 for v in strong_verbs if v in resume_text.lower())
        if verbs_present < 2:
            recommendations.append({
                "type": "ACTION_VERB",
                "title": "Strengthen Action Verbs in Bullet Points",
                "description": "Replace passive verbs like 'worked on' or 'helped with' with active engineering verbs.",
                "suggestion": "Lead with impactful verbs such as 'Spearheaded', 'Engineered', 'Optimized', 'Integrated', or 'Refactored'."
            })

        # 4. ATS Structural Checklist
        recommendations.append({
            "type": "FORMATTING",
            "title": "ATS Formatting Compliance",
            "description": "Standard ATS parsers parse standard section headings most reliably.",
            "suggestion": "Ensure headings use standard naming: 'Professional Summary', 'Technical Skills', 'Experience', 'Projects', 'Education'."
        })

        return recommendations
