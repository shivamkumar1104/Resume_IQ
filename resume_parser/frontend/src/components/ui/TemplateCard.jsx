const TEMPLATE_ICONS = {
  "Software Engineering":       "💻",
  "Data Science & AI":          "🤖",
  "Design & Product":           "🎨",
  "Leadership & Management":    "🎯",
}

function ScorePill({ score }) {
  const color = score >= 90 ? "#10b981" : score >= 80 ? "#6366f1" : "#f59e0b"
  return (
    <div style={{
      display: "flex", alignItems: "center", gap: 6,
      background: `${color}18`, border: `1px solid ${color}40`,
      borderRadius: 20, padding: "4px 12px"
    }}>
      <span style={{ fontSize: 11, fontWeight: 800, color, fontFamily: "JetBrains Mono, monospace" }}>
        {score}%
      </span>
      <span style={{ fontSize: 11, color: "var(--text-muted)", fontWeight: 500 }}>match</span>
    </div>
  )
}

export function TemplateCard({ template_id, name, category, compatibility_score, ats_friendly, key_features, index }) {
  const icon = TEMPLATE_ICONS[category] || "📄"
  return (
    <div className="card fade-in-up" style={{ padding: 20, animationDelay: `${index * 0.07}s` }}>
      <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12, marginBottom: 14 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{
            width: 44, height: 44, borderRadius: 12,
            background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.2)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 22, flexShrink: 0
          }}>
            {icon}
          </div>
          <div>
            <div style={{ fontWeight: 700, fontSize: 14, color: "var(--text-primary)", marginBottom: 3 }}>
              {name}
            </div>
            <div style={{ fontSize: 12, color: "var(--text-muted)" }}>{category}</div>
          </div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "flex-end", gap: 6, flexShrink: 0 }}>
          <ScorePill score={compatibility_score} />
          {ats_friendly && (
            <span style={{
              fontSize: 10, fontWeight: 700, color: "#10b981",
              background: "rgba(16,185,129,0.1)", border: "1px solid rgba(16,185,129,0.25)",
              padding: "2px 8px", borderRadius: 20, textTransform: "uppercase", letterSpacing: "0.05em"
            }}>
              ✓ ATS Friendly
            </span>
          )}
        </div>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
        {key_features.map((f, i) => (
          <div key={i} style={{ display: "flex", alignItems: "flex-start", gap: 8 }}>
            <span style={{ color: "#6366f1", fontSize: 12, marginTop: 1, flexShrink: 0 }}>▸</span>
            <span style={{ fontSize: 12, color: "var(--text-secondary)", lineHeight: 1.5 }}>{f}</span>
          </div>
        ))}
      </div>
    </div>
  )
}
