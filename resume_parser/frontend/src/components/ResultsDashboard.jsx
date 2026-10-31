import { useState } from "react"
import { ScoreRing, MiniScoreBar } from "./ui/ScoreRing.jsx"
import { SkillChip } from "./ui/SkillChip.jsx"
import { RecommendationCard } from "./ui/RecommendationCard.jsx"
import { TemplateCard } from "./ui/TemplateCard.jsx"

const STATUS_ICON = { PASS: "✅", WARN: "⚠️", FAIL: "❌" }

function SectionTab({ tabs, active, onSelect }) {
  return (
    <div style={{
      display: "flex", gap: 4, padding: "5px",
      background: "rgba(0,0,0,0.3)", borderRadius: 12, border: "1px solid rgba(255,255,255,0.06)",
      flexWrap: "wrap"
    }}>
      {tabs.map(tab => (
        <button
          key={tab.id}
          onClick={() => onSelect(tab.id)}
          style={{
            padding: "9px 18px", borderRadius: 9, border: "none", cursor: "pointer",
            fontWeight: 600, fontSize: 13, transition: "all 0.2s",
            background: active === tab.id ? "rgba(99,102,241,0.25)" : "transparent",
            color: active === tab.id ? "#a5b4fc" : "var(--text-muted)",
            borderBottom: active === tab.id ? "2px solid #6366f1" : "2px solid transparent"
          }}
        >
          {tab.icon} {tab.label}
        </button>
      ))}
    </div>
  )
}

function ContactCard({ contact, filename }) {
  return (
    <div className="card" style={{ padding: "20px 24px", display: "flex", alignItems: "flex-start", gap: 20, flexWrap: "wrap" }}>
      <div style={{
        width: 56, height: 56, borderRadius: 16, flexShrink: 0,
        background: "linear-gradient(135deg, rgba(99,102,241,0.25), rgba(6,182,212,0.15))",
        border: "2px solid rgba(99,102,241,0.3)",
        display: "flex", alignItems: "center", justifyContent: "center", fontSize: 24
      }}>👤</div>
      <div style={{ flex: 1 }}>
        <div style={{ fontWeight: 800, fontSize: 18, marginBottom: 4 }}>
          {contact?.name || "Candidate"}
        </div>
        <div style={{ fontSize: 12, color: "var(--text-muted)", marginBottom: 12 }}>📄 {filename}</div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 16 }}>
          {contact?.email && (
            <span style={{ fontSize: 13, color: "var(--text-secondary)", display: "flex", alignItems: "center", gap: 6 }}>
              📧 {contact.email}
            </span>
          )}
          {contact?.phone && (
            <span style={{ fontSize: 13, color: "var(--text-secondary)", display: "flex", alignItems: "center", gap: 6 }}>
              📱 {contact.phone}
            </span>
          )}
          {contact?.linkedin && (
            <a href={contact.linkedin.startsWith("http") ? contact.linkedin : `https://${contact.linkedin}`}
              target="_blank" rel="noopener noreferrer"
              style={{ fontSize: 13, color: "#6366f1", textDecoration: "none" }}>
              🔗 LinkedIn
            </a>
          )}
          {contact?.github && (
            <a href={contact.github.startsWith("http") ? contact.github : `https://${contact.github}`}
              target="_blank" rel="noopener noreferrer"
              style={{ fontSize: 13, color: "#8b5cf6", textDecoration: "none" }}>
              💻 GitHub
            </a>
          )}
        </div>
      </div>
    </div>
  )
}

function SkillsPanel({ skills }) {
  const matched = skills?.matched || []
  const missing = skills?.missing || []
  const all_candidate = skills?.all_candidate_skills || []

  const groupBy = (items) => {
    const groups = {}
    items.forEach(s => {
      const cat = s.category || "General"
      if (!groups[cat]) groups[cat] = []
      groups[cat].push(s)
    })
    return groups
  }

  return (
    <div>
      {/* Summary pills */}
      <div style={{ display: "flex", gap: 12, marginBottom: 28, flexWrap: "wrap" }}>
        {[
          { label: `${matched.filter(s => s.match_type === "EXACT").length} Exact`, color: "#10b981", bg: "rgba(16,185,129,0.12)" },
          { label: `${matched.filter(s => s.match_type === "SEMANTIC").length} Related`, color: "#f59e0b", bg: "rgba(245,158,11,0.12)" },
          { label: `${missing.length} Missing`, color: "#f43f5e", bg: "rgba(244,63,94,0.12)" },
          { label: `${all_candidate.length} Total Detected`, color: "#8b5cf6", bg: "rgba(139,92,246,0.12)" },
        ].map((pill, i) => (
          <div key={i} style={{
            padding: "6px 14px", borderRadius: 20, fontSize: 13, fontWeight: 700,
            color: pill.color, background: pill.bg, border: `1px solid ${pill.color}30`
          }}>{pill.label}</div>
        ))}
      </div>

      {matched.length > 0 && (
        <div style={{ marginBottom: 28 }}>
          <div style={{ fontSize: 12, fontWeight: 700, color: "#10b981", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 12 }}>
            ✓ JD Skill Matches
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {matched.map((s, i) => <SkillChip key={i} {...s} matchType={s.match_type} />)}
          </div>
        </div>
      )}

      {missing.length > 0 && (
        <div style={{ marginBottom: 28 }}>
          <div style={{ fontSize: 12, fontWeight: 700, color: "#f43f5e", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 12 }}>
            ✗ Missing JD Requirements
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {missing.map((s, i) => <SkillChip key={i} {...s} matchType="MISSING" />)}
          </div>
        </div>
      )}

      {all_candidate.length > 0 && (
        <div>
          <div style={{ fontSize: 12, fontWeight: 700, color: "#8b5cf6", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 12 }}>
            ● All Detected Candidate Skills
          </div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {all_candidate.map((s, i) => (
              <SkillChip key={i} {...s} matchType={s.category === "Domain Specific / Discovered" ? "DISCOVERED" : "EXACT"} />
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

function ATSPanel({ ats_report }) {
  if (!ats_report) return null
  const { overall_score, grade, checks, priority_fixes, word_count } = ats_report
  const gradeColor = overall_score >= 80 ? "#10b981" : overall_score >= 65 ? "#6366f1" : overall_score >= 50 ? "#f59e0b" : "#f43f5e"

  return (
    <div>
      {/* ATS Score header */}
      <div style={{ display: "flex", alignItems: "center", gap: 24, marginBottom: 32, flexWrap: "wrap" }}>
        <div style={{
          display: "flex", alignItems: "center", gap: 16, padding: "20px 28px",
          background: `${gradeColor}12`, border: `1px solid ${gradeColor}30`, borderRadius: 16
        }}>
          <div style={{ fontSize: 48, fontWeight: 900, color: gradeColor, fontFamily: "JetBrains Mono, monospace", lineHeight: 1 }}>
            {grade}
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: 22, color: gradeColor }}>{overall_score}%</div>
            <div style={{ fontSize: 13, color: "var(--text-muted)" }}>ATS Score · {word_count} words</div>
          </div>
        </div>
        {priority_fixes?.length > 0 && (
          <div style={{ flex: 1, minWidth: 200 }}>
            <div style={{ fontSize: 12, fontWeight: 700, color: "var(--text-muted)", marginBottom: 10, textTransform: "uppercase", letterSpacing: "0.08em" }}>
              Top Impact Fixes
            </div>
            {priority_fixes.map((fix, i) => (
              <div key={i} style={{
                display: "flex", gap: 10, marginBottom: 8, alignItems: "flex-start",
                fontSize: 13, color: "var(--text-secondary)"
              }}>
                <span style={{
                  width: 20, height: 20, background: "rgba(244,63,94,0.15)", borderRadius: 6,
                  display: "flex", alignItems: "center", justifyContent: "center",
                  fontSize: 10, fontWeight: 800, color: "#f43f5e", flexShrink: 0
                }}>{fix.priority}</span>
                <span>{fix.label} <span style={{ color: "#10b981", fontWeight: 700 }}>({fix.impact})</span></span>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Per-check list */}
      <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
        {checks.map((check, i) => (
          <div key={check.id} className="card fade-in-up"
            style={{ padding: "16px 20px", animationDelay: `${i * 0.06}s` }}>
            <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
              <span style={{ fontSize: 18, flexShrink: 0 }}>{STATUS_ICON[check.status]}</span>
              <div style={{ flex: 1 }}>
                <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 8, gap: 12, flexWrap: "wrap" }}>
                  <span style={{ fontWeight: 600, fontSize: 14 }}>{check.label}</span>
                  <span style={{
                    fontFamily: "JetBrains Mono, monospace", fontSize: 13, fontWeight: 700,
                    color: check.status === "PASS" ? "#10b981" : check.status === "WARN" ? "#f59e0b" : "#f43f5e"
                  }}>{check.score}/{check.max_score}</span>
                </div>
                <div className="progress-bar">
                  <div className="progress-fill" style={{
                    width: `${(check.score / check.max_score) * 100}%`,
                    background: check.status === "PASS"
                      ? "linear-gradient(90deg, #10b981aa, #10b981)"
                      : check.status === "WARN"
                      ? "linear-gradient(90deg, #f59e0baa, #f59e0b)"
                      : "linear-gradient(90deg, #f43f5eaa, #f43f5e)",
                    transition: `width ${0.8 + i * 0.1}s cubic-bezier(0.25,1,0.5,1)`
                  }} />
                </div>
                {check.issues?.length > 0 && (
                  <div style={{ marginTop: 8 }}>
                    {check.issues.slice(0, 2).map((issue, j) => (
                      <div key={j} style={{ fontSize: 12, color: "var(--text-muted)", marginTop: 3 }}>
                        • {issue}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

const TABS = [
  { id: "overview",   icon: "📊", label: "Score Overview" },
  { id: "skills",     icon: "🧠", label: "Skill Analysis" },
  { id: "ats",        icon: "🔍", label: "ATS Report" },
  { id: "ai",         icon: "✍️", label: "AI Suggestions" },
  { id: "templates",  icon: "📋", label: "Templates" },
]

export function ResultsDashboard({ result, onReset }) {
  const [activeTab, setActiveTab] = useState("overview")
  if (!result) return null

  const {
    filename = "Resume",
    contact = {},
    scores = {},
    skills = {},
    ats_report = {},
    improvements = [],
    recommended_templates = [],
    processing_time_ms = 0,
  } = result

  return (
    <div style={{ minHeight: "100vh" }}>
      {/* Sticky header */}
      <div style={{
        position: "sticky", top: 0, zIndex: 50,
        background: "rgba(6,9,19,0.92)", backdropFilter: "blur(20px)",
        borderBottom: "1px solid rgba(255,255,255,0.05)"
      }}>
        <div style={{
          maxWidth: 1200, margin: "0 auto",
          padding: "14px 32px",
          display: "flex", alignItems: "center", justifyContent: "space-between", gap: 16, flexWrap: "wrap"
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
            <div style={{
              width: 32, height: 32, borderRadius: 9,
              background: "linear-gradient(135deg, #6366f1, #06b6d4)",
              display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15
            }}>🎯</div>
            <span style={{ fontWeight: 800, fontSize: 15 }}>ResumeIQ</span>
            <span style={{ fontSize: 12, color: "var(--text-muted)", paddingLeft: 8, borderLeft: "1px solid rgba(255,255,255,0.1)" }}>
              Analysis complete · {processing_time_ms}ms
            </span>
          </div>
          <button className="btn-secondary" style={{ fontSize: 12, padding: "7px 16px" }} onClick={onReset}>
            ← New Analysis
          </button>
        </div>
        <div style={{ maxWidth: 1200, margin: "0 auto", padding: "0 32px 12px" }}>
          <SectionTab tabs={TABS} active={activeTab} onSelect={setActiveTab} />
        </div>
      </div>

      {/* Content */}
      <div style={{ maxWidth: 1200, margin: "0 auto", padding: "32px 32px 80px" }}>
        {/* Contact card always visible */}
        <div style={{ marginBottom: 28 }}>
          <ContactCard contact={contact} filename={filename} />
        </div>

        {/* ── Overview Tab ── */}
        {activeTab === "overview" && (
          <div className="fade-in-up">
            <div style={{ display: "grid", gridTemplateColumns: "auto 1fr", gap: 28, alignItems: "start", flexWrap: "wrap" }}>
              <div className="card" style={{ padding: "36px 40px", display: "flex", justifyContent: "center" }}>
                <ScoreRing score={scores.final_score ?? 0} size={200} label="Overall Fit Score" />
              </div>
              <div className="card" style={{ padding: "28px 32px" }}>
                <div style={{ fontSize: 13, fontWeight: 700, color: "var(--text-muted)", textTransform: "uppercase", letterSpacing: "0.1em", marginBottom: 20 }}>
                  Score Breakdown
                </div>
                <MiniScoreBar label="Skill Coverage"        score={scores.skill_coverage ?? 0}     color="#10b981" delay={0} />
                <MiniScoreBar label="Experience Match"      score={scores.experience_score ?? 0}   color="#6366f1" delay={100} />
                <MiniScoreBar label="Projects Score"        score={scores.projects_score ?? 0}     color="#8b5cf6" delay={200} />
                <MiniScoreBar label="Education Score"       score={scores.education_score ?? 0}    color="#06b6d4" delay={300} />
                <MiniScoreBar label="Semantic Similarity"   score={scores.semantic_similarity ?? 0} color="#3b82f6" delay={400} />
                <MiniScoreBar label="ATS Compliance"        score={scores.ats_score ?? ats_report?.overall_score ?? 0} color="#f59e0b" delay={500} />
                <div style={{ marginTop: 20, padding: "12px 16px", background: "rgba(255,255,255,0.03)", borderRadius: 10, display: "flex", gap: 24, flexWrap: "wrap" }}>
                  <div style={{ fontSize: 13, color: "var(--text-muted)" }}>
                    📅 <strong style={{ color: "var(--text-primary)" }}>{scores.experience_years_detected ?? 0}y</strong> exp detected
                  </div>
                  <div style={{ fontSize: 13, color: "var(--text-muted)" }}>
                    🔨 <strong style={{ color: "var(--text-primary)" }}>{scores.project_count_detected ?? 0}</strong> project(s) found
                  </div>
                  <div style={{ fontSize: 13, color: "var(--text-muted)" }}>
                    🎯 ATS Grade: <strong style={{
                      color: (scores.ats_score ?? ats_report?.overall_score ?? 0) >= 80 ? "#10b981" : (scores.ats_score ?? ats_report?.overall_score ?? 0) >= 65 ? "#f59e0b" : "#f43f5e"
                    }}>{ats_report?.grade || "—"}</strong>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* ── Skills Tab ── */}
        {activeTab === "skills" && (
          <div className="card fade-in-up" style={{ padding: "28px 32px" }}>
            <SkillsPanel skills={skills} />
          </div>
        )}

        {/* ── ATS Tab ── */}
        {activeTab === "ats" && (
          <div className="fade-in-up">
            <ATSPanel ats_report={ats_report} />
          </div>
        )}

        {/* ── AI Suggestions Tab ── */}
        {activeTab === "ai" && (
          <div className="fade-in-up" style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            <div style={{ marginBottom: 8 }}>
              <h2 style={{ fontWeight: 800, fontSize: 22, marginBottom: 6 }}>AI Improvement Suggestions</h2>
              <p style={{ fontSize: 14, color: "var(--text-muted)" }}>
                Grounded in candidate experience — zero hallucination, 100% verified recommendations
              </p>
            </div>
            {improvements?.length > 0 ? improvements.map((rec, i) => (
              <RecommendationCard key={i} {...rec} index={i} />
            )) : (
              <div style={{ textAlign: "center", padding: 40, color: "var(--text-muted)", fontSize: 15 }}>
                ✅ No major improvements needed!
              </div>
            )}
          </div>
        )}

        {/* ── Templates Tab ── */}
        {activeTab === "templates" && (
          <div className="fade-in-up">
            <div style={{ marginBottom: 24 }}>
              <h2 style={{ fontWeight: 800, fontSize: 22, marginBottom: 6 }}>Recommended Resume Templates</h2>
              <p style={{ fontSize: 14, color: "var(--text-muted)" }}>
                Ranked by compatibility with this candidate and role
              </p>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(340px, 1fr))", gap: 16 }}>
              {recommended_templates?.map((t, i) => (
                <TemplateCard key={i} {...t} index={i} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
