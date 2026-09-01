import { useState } from "react"

const MATCH_CONFIG = {
  EXACT:      { cls: "chip-exact",      dot: "#10b981", label: "Exact" },
  SEMANTIC:   { cls: "chip-semantic",   dot: "#f59e0b", label: "Related" },
  MISSING:    { cls: "chip-missing",    dot: "#f43f5e", label: "Missing" },
  DISCOVERED: { cls: "chip-discovered", dot: "#8b5cf6", label: "Discovered" },
}

export function SkillChip({ skill, matchType = "EXACT", confidence, evidence, category }) {
  const [showTip, setShowTip] = useState(false)
  const cfg = MATCH_CONFIG[matchType] || MATCH_CONFIG.EXACT

  return (
    <div
      className="tooltip-wrapper"
      onMouseEnter={() => setShowTip(true)}
      onMouseLeave={() => setShowTip(false)}
      style={{ display: "inline-flex" }}
    >
      <span className={`chip ${cfg.cls}`}>
        <span style={{
          width: 6, height: 6, borderRadius: "50%",
          background: cfg.dot, display: "inline-block", flexShrink: 0
        }} />
        {skill}
        {confidence && (
          <span style={{
            fontSize: 10, opacity: 0.7,
            fontFamily: "JetBrains Mono, monospace"
          }}>
            {Math.round(confidence * 100)}%
          </span>
        )}
      </span>
      {showTip && (evidence || category) && (
        <div className="tooltip" style={{ opacity: 1, minWidth: 200, maxWidth: 300 }}>
          {category && (
            <div style={{ color: "var(--accent-primary)", fontSize: 10, fontWeight: 700, marginBottom: 4, textTransform: "uppercase", letterSpacing: "0.06em" }}>
              {category}
            </div>
          )}
          {evidence && (
            <div style={{ fontSize: 12, lineHeight: 1.5, color: "var(--text-secondary)" }}>
              "{evidence.length > 150 ? evidence.slice(0, 150) + "…" : evidence}"
            </div>
          )}
          <div style={{ marginTop: 6, fontSize: 10, color: cfg.dot, fontWeight: 700 }}>
            ● {cfg.label} Match
          </div>
        </div>
      )}
    </div>
  )
}

export function SkillCategoryGroup({ category, skills }) {
  if (!skills || skills.length === 0) return null
  return (
    <div style={{ marginBottom: 20 }}>
      <div className="section-label" style={{ marginBottom: 10 }}>{category}</div>
      <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
        {skills.map((s, i) => (
          <SkillChip
            key={i}
            skill={s.skill}
            matchType={s.match_type}
            confidence={s.confidence}
            evidence={s.evidence}
            category={s.category}
          />
        ))}
      </div>
    </div>
  )
}
