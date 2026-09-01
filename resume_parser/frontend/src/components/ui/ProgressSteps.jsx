export function ProgressSteps({ steps, currentStep, progress }) {
  return (
    <div style={{ width: "100%", maxWidth: 520, margin: "0 auto" }}>
      {/* Progress bar */}
      <div className="progress-bar" style={{ height: 4, marginBottom: 32 }}>
        <div className="progress-fill" style={{
          width: `${progress}%`,
          background: "linear-gradient(90deg, #6366f1, #06b6d4)"
        }} />
      </div>
      {/* Steps */}
      <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
        {steps.map((step, i) => {
          const isDone    = i < currentStep
          const isCurrent = i === currentStep
          const isPending = i > currentStep
          return (
            <div
              key={step.id}
              style={{
                display: "flex", alignItems: "center", gap: 16,
                opacity: isPending ? 0.35 : 1,
                transition: "opacity 0.3s"
              }}
            >
              {/* Icon circle */}
              <div style={{
                width: 40, height: 40, borderRadius: "50%", flexShrink: 0,
                display: "flex", alignItems: "center", justifyContent: "center",
                fontSize: 18,
                background: isDone
                  ? "rgba(16,185,129,0.15)"
                  : isCurrent
                  ? "rgba(99,102,241,0.2)"
                  : "rgba(255,255,255,0.04)",
                border: isDone
                  ? "2px solid rgba(16,185,129,0.5)"
                  : isCurrent
                  ? "2px solid rgba(99,102,241,0.6)"
                  : "2px solid rgba(255,255,255,0.06)",
                transition: "all 0.4s"
              }}>
                {isDone ? "✓" : step.icon}
              </div>
              {/* Label */}
              <div>
                <div style={{
                  fontSize: 14, fontWeight: isCurrent ? 700 : 500,
                  color: isDone ? "#10b981" : isCurrent ? "#a5b4fc" : "var(--text-muted)",
                  transition: "color 0.3s"
                }}>
                  {step.label}
                </div>
                {isCurrent && (
                  <div style={{ fontSize: 12, color: "var(--text-muted)", marginTop: 2 }}>
                    <span className="pulse-dot" style={{ display: "inline-block", width: 6, height: 6, background: "#6366f1", borderRadius: "50%", marginRight: 6 }} />
                    Processing…
                  </div>
                )}
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
