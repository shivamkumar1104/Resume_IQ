"""Company-Ready Resume Template Recommendation and Ranking Engine."""

from typing import List, Dict, Any

COMPANY_TEMPLATES = [
    {
        "template_id": "ats_software_modern",
        "name": "Modern ATS Software Engineer",
        "category": "Software Engineering",
        "keywords": ["react", "node", "python", "full stack", "backend", "frontend", "developer", "software", "api", "cloud"],
        "ats_friendly": True,
        "key_features": [
            "Single-column ATS compliant structure",
            "Prominent Core Skills & Tech Stack matrix",
            "Quantifiable impact-focused Project bullet format (X-Y-Z)",
            "Optimized for standard applicant tracking systems (Greenhouse, Lever)"
        ]
    },
    {
        "template_id": "ats_data_analytics",
        "name": "Data Analyst & AI Specialist",
        "category": "Data Science & AI",
        "keywords": ["data", "machine learning", "python", "sql", "analytics", "power bi", "tableau", "ai", "deep learning"],
        "ats_friendly": True,
        "key_features": [
            "Data Pipeline & Modeling skill highlights",
            "Key Metrics & Business Impact callouts",
            "Tooling breakdown (Languages, Frameworks, BI Tools)"
        ]
    },
    {
        "template_id": "ats_product_design",
        "name": "Product & UX Designer Portfolio Resume",
        "category": "Design & Product",
        "keywords": ["design", "figma", "ui/ux", "user experience", "product design", "prototyping", "research"],
        "ats_friendly": True,
        "key_features": [
            "Clean layout with Portfolio & Case Study links",
            "User Research & Prototyping process focus",
            "Cross-functional collaboration bullet structure"
        ]
    },
    {
        "template_id": "ats_executive_classic",
        "name": "Executive & Senior Leadership Classic",
        "category": "Leadership & Management",
        "keywords": ["lead", "manager", "director", "architect", "strategy", "roadmap", "agile", "leadership"],
        "ats_friendly": True,
        "key_features": [
            "Strategic Executive Summary header",
            "Team scale, budget, and delivery achievements",
            "Chronological career trajectory design"
        ]
    }
]


class TemplateEngine:
    """Ranks and recommends standard company hiring resume templates."""

    def recommend_templates(self, jd_text: str, candidate_skills: List[str]) -> List[Dict[str, Any]]:
        """
        Score and rank templates based on relevance to target job and skills.
        """
        combined_text = (jd_text + " " + " ".join(candidate_skills)).lower()
        scored_templates = []

        for t in COMPANY_TEMPLATES:
            matched_keywords = sum(1 for kw in t["keywords"] if kw in combined_text)
            match_score = min(98.0, 75.0 + (matched_keywords * 4.5))

            scored_templates.append({
                "template_id": t["template_id"],
                "name": t["name"],
                "category": t["category"],
                "compatibility_score": round(match_score, 1),
                "ats_friendly": t["ats_friendly"],
                "key_features": t["key_features"]
            })

        # Sort descending by compatibility score
        scored_templates.sort(key=lambda x: x["compatibility_score"], reverse=True)
        return scored_templates
