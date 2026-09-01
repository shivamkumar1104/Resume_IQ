"""Pydantic schemas for screening API requests and responses."""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class ContactInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class SkillMatchItem(BaseModel):
    skill: str
    category: str = "General"
    match_type: str  # "EXACT", "SEMANTIC", "MISSING"
    confidence: float = 1.0
    evidence: Optional[str] = None


class ScoreBreakdown(BaseModel):
    final_score: float = Field(..., description="Weighted candidate fit score (0-100%)")
    semantic_similarity: float = Field(..., description="Sentence transformer semantic score (0-100%)")
    skill_coverage: float = Field(..., description="Explicit skill match ratio (0-100%)")
    ats_score: float = Field(..., description="ATS structure and keyword score (0-100%)")


class TemplateRecommendation(BaseModel):
    template_id: str
    name: str
    category: str
    compatibility_score: float
    ats_friendly: bool = True
    key_features: List[str]
    sample_preview_url: Optional[str] = None


class ResumeImprovement(BaseModel):
    type: str  # "CRITICAL_SKILL", "ACTION_VERB", "QUANTIFICATION", "FORMATTING"
    title: str
    description: str
    suggestion: str


class ScreeningResult(BaseModel):
    filename: str
    contact: ContactInfo
    scores: ScoreBreakdown
    skills: Dict[str, List[SkillMatchItem]]
    improvements: List[ResumeImprovement]
    recommended_templates: List[TemplateRecommendation]
    processing_time_ms: int
