import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "Resume Intelligence Platform — Production Architecture & Engineering Blueprint")
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
            
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 36, page_text)
        self.drawString(54, 36, "CONFIDENTIAL & PROPRIETARY — RESUME INTELLIGENCE ARCHITECTURE")
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(54, 48, 558, 48)
        
        self.restoreState()

def build_pdf(filename="Resume_Intelligence_Master_Blueprint.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=colors.HexColor('#0F172A'),
        alignment=0,
        spaceAfter=8
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#475569'),
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor('#2563EB'),
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor('#0F172A'),
        backColor=colors.HexColor('#F8FAFC'),
        borderColor=colors.HexColor('#E2E8F0'),
        borderWidth=1,
        borderPadding=6,
        spaceBefore=4,
        spaceAfter=6
    )

    story = []

    # Title Banner
    story.append(Paragraph("Resume Intelligence Platform", title_style))
    story.append(Paragraph("Comprehensive Production Architecture, AI Engineering Pipeline & Complete Implementation Roadmap", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563EB"), spaceAfter=14))

    # Meta table
    meta_data = [
        [Paragraph("<b>Target System:</b> Production AI Resume Screener & Recruiter Engine", body_style),
         Paragraph("<b>Date:</b> August 2026", body_style)],
        [Paragraph("<b>Architecture:</b> Monorepo (Next.js 14 + NestJS + Redis/BullMQ + Python AI)", body_style),
         Paragraph("<b>Database:</b> PostgreSQL + pgvector", body_style)]
    ]
    meta_table = Table(meta_data, colWidths=[280, 224])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F1F5F9')),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LINEBELOW', (0, -1), (-1, -1), 1, colors.HexColor('#CBD5E1')),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # 1. Executive Summary
    story.append(Paragraph("1. Executive Summary & Core Value Proposition", h1_style))
    story.append(Paragraph(
        "The <b>Resume Intelligence Platform</b> is an enterprise-grade AI hiring platform that elevates resume parsing from a basic keyword-matching script into an intelligent talent evaluation engine. Rather than relying on rigid, pre-defined skill whitelists, it dynamically extracts candidate attributes, computes explainable match scores with evidence, evaluates ATS compatibility with actionable diagnostics, and renders executive company-ready suggestion templates.",
        body_style
    ))

    # 2. Production Monorepo Architecture
    story.append(Paragraph("2. System Architecture & Monorepo Topology", h1_style))
    story.append(Paragraph("The platform adopts a high-performance modular monorepo structure designed for clean separation of concerns and independent scalability:", body_style))
    
    arch_code = (
        "resume-intelligence/<br/>"
        "├── apps/<br/>"
        "│   ├── web/          # Next.js 14 Frontend (App Router, Tailwind, shadcn/ui)<br/>"
        "│   ├── api/          # NestJS Core API (Auth, RBAC, DB CRUD, Queue Producer)<br/>"
        "│   └── worker/       # BullMQ Background Worker (Document pipeline execution)<br/>"
        "├── services/ai/      # Python FastAPI Microservice (NLP, LLM, Embeddings, SpaCy)<br/>"
        "├── packages/        # Shared packages (types, validation/zod schemas, config)<br/>"
        "└── infrastructure/  # Docker, Nginx, PostgreSQL + pgvector, Redis"
    )
    story.append(Paragraph(arch_code, code_style))

    # 3. Core AI & Technical Subsystems
    story.append(Paragraph("3. Core Subsystems & Technical Pipelines", h1_style))

    story.append(Paragraph("3.1 Universal Open-Ended Skill Extraction", h2_style))
    story.append(Paragraph(
        "<b>No Hardcoded Whitelists:</b> Traditional parsers fail when encountering modern, niche, or domain-specific skills (e.g. <i>'Temporal, LangGraph, OpenTelemetry, RAGAS'</i>). The system utilizes a multi-tiered pipeline: Candidate Phrase Detection → Semantic LLM Extraction → Canonical Normalization (e.g. 'React.js / ReactJS' → 'React.js') → Dynamic Categorization → Confidence & Evidence Binding.",
        body_style
    ))

    story.append(Paragraph("3.2 Explainable Job Matching Engine", h2_style))
    story.append(Paragraph(
        "Scores are not opaque black boxes. Every match score includes an explicit breakdown and concrete evidence linking:",
        body_style
    ))
    story.append(Paragraph("• <b>Composite Scoring Formula:</b> <code>Overall = (Skills * 0.40) + (Experience * 0.25) + (Projects * 0.20) + (Education * 0.05) + (Semantic Sim * 0.10)</code>", bullet_style))
    story.append(Paragraph("• <b>Evidence Traceability:</b> Associates each matched skill with specific projects or roles in the candidate's history.", bullet_style))

    story.append(Paragraph("3.3 ATS Compatibility Engine", h2_style))
    story.append(Paragraph(
        "Evaluates parsing compliance, section hierarchy, quantified achievement metrics (X-Y-Z formula), job title alignment, and provides high-impact recommendations.",
        body_style
    ))

    story.append(Paragraph("3.4 Grounded AI Resume Suggestions & Company Templates", h2_style))
    story.append(Paragraph(
        "Strictly grounded in verified candidate experience without fabricating credentials. Generates standardized company hiring templates: <i>Recruiter Screening Summaries, Interview Focus Checklists, Shortlist Memos, and Constructive Feedback Letters.</i>",
        body_style
    ))

    story.append(Spacer(1, 8))

    # 4. Database Schema
    story.append(Paragraph("4. Relational & Vector Database Schema (PostgreSQL + pgvector)", h1_style))
    
    schema_data = [
        ["Table", "Primary Fields", "Description"],
        ["users", "id, name, email, password_hash, role", "Candidates, Recruiters, and Admins"],
        ["resumes", "id, user_id, file_url, status, file_hash", "Raw file tracking & processing state machine"],
        ["candidate_profiles", "id, resume_id, name, email, phone, summary, exp", "Parsed candidate structured information"],
        ["skills", "id, canonical_name, category, embedding", "Global catalog of normalized skills with vector embeddings"],
        ["candidate_skills", "id, candidate_id, skill_id, confidence, source, evidence", "Skill associations with confidence score & provenance"],
        ["jobs", "id, organization_id, title, description, exp_min, exp_max", "Target job description requirements"],
        ["job_skills", "id, job_id, skill_id, importance, required", "Required vs preferred skills for role"],
        ["matches", "id, candidate_id, job_id, overall_score, breakdown", "Detailed evaluation scores"],
        ["match_evidence", "id, match_id, skill_id, candidate_evidence, reason", "Explainability layer for auditability"],
        ["templates", "id, name, type, content, variables", "Standardized hiring templates"]
    ]
    
    table_rows = []
    for r in schema_data:
        table_rows.append([
            Paragraph(f"<b>{r[0]}</b>", body_style),
            Paragraph(f"<code>{r[1]}</code>", body_style),
            Paragraph(r[2], body_style)
        ])
    
    schema_table = Table(table_rows, colWidths=[95, 205, 204])
    schema_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#E2E8F0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0F172A')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(schema_table)

    story.append(Spacer(1, 10))

    # 5. REST API Architecture
    story.append(Paragraph("5. REST API Specifications (/api/v1)", h1_style))
    story.append(Paragraph("• <code>POST /api/v1/resumes/upload</code> - Accepts multipart PDF/DOCX, creates async BullMQ job (returns 202 Accepted).", bullet_style))
    story.append(Paragraph("• <code>GET /api/v1/resumes/:id/status</code> - Polls processing state (QUEUED → EXTRACTING → SKILL_ANALYSIS → COMPLETED).", bullet_style))
    story.append(Paragraph("• <code>GET /api/v1/candidates/:id/profile</code> - Retrieves structured profile, contact info, and categorized skills.", bullet_style))
    story.append(Paragraph("• <code>POST /api/v1/jobs</code> & <code>POST /api/v1/matches</code> - Creates target roles and triggers matching evaluation.", bullet_style))
    story.append(Paragraph("• <code>POST /api/v1/templates/:id/generate</code> - Renders hiring recommendation documents populated with candidate intelligence.", bullet_style))

    story.append(Spacer(1, 8))

    # 6. Implementation Roadmap
    story.append(Paragraph("6. 12-Stage Implementation Roadmap", h1_style))
    
    roadmap_data = [
        ["Phase", "Milestone Focus", "Key Deliverables"],
        ["Phase 1", "Monorepo & Infra", "Docker (Postgres + Redis), Next.js, NestJS, Python FastAPI, Turborepo"],
        ["Phase 2", "Data Layer & Auth", "Prisma migrations, JWT auth, RBAC (Candidate/Recruiter), S3 upload storage"],
        ["Phase 3", "Async Ingestion Worker", "BullMQ queue, PDF/DOCX text extraction, layout & section boundary detection"],
        ["Phase 4", "Universal Skill Engine", "Dynamic LLM/SpaCy extraction, canonical mapping, category tagging & confidence"],
        ["Phase 5", "ATS Diagnostic Engine", "Section completeness, bullet impact scoring, keyword density analysis"],
        ["Phase 6", "JD Parser & Matching", "Dense embeddings, multi-factor weighted scoring, evidence linking"],
        ["Phase 7", "AI Improvement Engine", "Targeted bullet rewrites (X-Y-Z formula) without hallucination"],
        ["Phase 8", "Template Generation", "Recruiter screening summaries, interview guides, shortlist memos"],
        ["Phase 9", "Recruiter Dashboard", "Candidate ranking table, pipeline kanban, skill breakdown charts"],
        ["Phase 10", "Production Hardening", "Rate limiting, Redis caching, structured logging, OpenAPI documentation"],
        ["Phase 11", "Testing & Verification", "Unit test suite (PyTest + Jest), E2E test suite (Playwright)"],
        ["Phase 12", "Cloud Deployment", "CI/CD GitHub Actions, Container registry, Cloud DB & Redis setup"]
    ]

    r_rows = []
    for r in roadmap_data:
        r_rows.append([
            Paragraph(f"<b>{r[0]}</b>", body_style),
            Paragraph(r[1], body_style),
            Paragraph(r[2], body_style)
        ])

    roadmap_table = Table(r_rows, colWidths=[65, 130, 309])
    roadmap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(roadmap_table)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Master Blueprint PDF successfully generated at: {filename}")

if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "Resume_Intelligence_Master_Blueprint.pdf"
    build_pdf(out)
