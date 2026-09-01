const TYPE_CONFIG = {
  CRITICAL_SKILL: { icon: "🚨", color: "#f43f5e", bg: "rgba(244,63,94,0.08)", border: "#f43f5e", cls: "rec-critical", label: "Critical Skill Gap" },
  ACTION_VERB:    { icon: "⚡", color: "#f59e0b", bg: "rgba(245,158,11,0.08)", border: "#f59e0b", cls: "rec-action",   label: "Action Verbs" },
  QUANTIFICATION: { icon: "📊", color: "#3b82f6", bg: "rgba(59,130,246,0.08)", border: "#3b82f6", cls: "rec-quant",   label: "Quantification" },
  FORMATTING:     { icon: "✅", color: "#06b6d4", bg: "rgba(6,182,212,0.08)",  border: "#06b6d4", cls: "rec-format",  label: "ATS Formatting" },
}

export function RecommendationCard({ type, title, description, suggestion, index }) {
  const cfg = TYPE_CONFIG[type] || TYPE_CONFIG.FORMATTING
  return (
    <div
      className={`card fade-in-up`}
      style={{
        padding: "20px 20px 20px 24px",
        animationDelay: `${index * 0.08}s`,
        borderLeft: `3px solid ${cfg.border}`,
        background: cfg.bg,
      }}
    >
      <div style={{ display: "flex", alignItems: "flex-start", gap: 14 }}>
        <div style={{
          width: 38, height: 38, borderRadius: 10,
          background: `${cfg.color}22`,
          display: "flex", alignItems: "center", justifyContent: "center",
          fontSize: 18, flexShrink: 0
        }}>
          {cfg.icon}
        </div>
        <div style={{ flex: 1, minWidth: 0 }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 6, flexWrap: "wrap" }}>
            <span style={{ fontSize: 14, fontWeight: 700, color: "var(--text-primary)" }}>{title}</span>
            <span style={{
              fontSize: 10, fontWeight: 700, color: cfg.color,
              background: `${cfg.color}20`, border: `1px solid ${cfg.color}40`,
              padding: "2px 8px", borderRadius: 20, textTransform: "uppercase", letterSpacing: "0.05em"
            }}>{cfg.label}</span>
          </div>
          <p style={{ fontSize: 13, color: "var(--text-secondary)", marginBottom: 10, lineHeight: 1.6 }}>
            {description}
          </p>
          <div style={{
            fontSize: 13, color: "var(--text-primary)", lineHeight: 1.6,
            background: "rgba(255,255,255,0.04)", borderRadius: 8,
            padding: "10px 14px",
            borderLeft: `2px solid ${cfg.color}60`
          }}>
            <span style={{ color: cfg.color, fontWeight: 700, marginRight: 6 }}>→</span>
            {suggestion}
          </div>
        </div>
      </div>
    </div>
  )
}
