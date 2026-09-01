import { useEffect, useRef, useState } from "react"

const SCORE_COLORS = {
  excellent: { stroke: "#10b981", glow: "rgba(16,185,129,0.4)" },
  good:      { stroke: "#6366f1", glow: "rgba(99,102,241,0.4)" },
  fair:      { stroke: "#f59e0b", glow: "rgba(245,158,11,0.4)" },
  poor:      { stroke: "#f43f5e", glow: "rgba(244,63,94,0.4)" },
}

function getColorTier(score) {
  if (score >= 80) return SCORE_COLORS.excellent
  if (score >= 65) return SCORE_COLORS.good
  if (score >= 45) return SCORE_COLORS.fair
  return SCORE_COLORS.poor
}

function getLabel(score) {
  if (score >= 80) return "Excellent Match"
  if (score >= 65) return "Good Match"
  if (score >= 45) return "Fair Match"
  return "Low Match"
}

export function ScoreRing({ score = 0, size = 200, label = "Overall Fit" }) {
  const [animatedScore, setAnimatedScore] = useState(0)
  const animRef = useRef(null)

  const radius = (size - 28) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (animatedScore / 100) * circumference
  const colors = getColorTier(score)

  useEffect(() => {
    let start = null
    const duration = 1500
    const animate = (ts) => {
      if (!start) start = ts
      const elapsed = ts - start
      const progress = Math.min(elapsed / duration, 1)
      // ease-out-cubic
      const eased = 1 - Math.pow(1 - progress, 3)
      setAnimatedScore(Math.round(eased * score))
      if (progress < 1) animRef.current = requestAnimationFrame(animate)
    }
    const timeout = setTimeout(() => {
      animRef.current = requestAnimationFrame(animate)
    }, 200)
    return () => {
      clearTimeout(timeout)
      if (animRef.current) cancelAnimationFrame(animRef.current)
    }
  }, [score])

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12 }}>
      <svg
        width={size}
        height={size}
        className="score-ring-svg"
        style={{ filter: `drop-shadow(0 0 16px ${colors.glow})` }}
      >
        {/* Background track */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="rgba(255,255,255,0.05)"
          strokeWidth={12}
        />
        {/* Progress arc */}
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={colors.stroke}
          strokeWidth={12}
          strokeLinecap="round"
          strokeDasharray={circumference}
          strokeDashoffset={offset}
          transform={`rotate(-90 ${size / 2} ${size / 2})`}
        />
        {/* Score text */}
        <text
          x={size / 2}
          y={size / 2 - 6}
          textAnchor="middle"
          fill={colors.stroke}
          fontSize={size * 0.22}
          fontWeight="900"
          fontFamily="Inter, sans-serif"
          letterSpacing="-2"
        >
          {animatedScore}
        </text>
        <text
          x={size / 2}
          y={size / 2 + 18}
          textAnchor="middle"
          fill="rgba(255,255,255,0.4)"
          fontSize={size * 0.07}
          fontWeight="600"
          fontFamily="Inter, sans-serif"
        >
          / 100
        </text>
      </svg>
      <div style={{ textAlign: "center" }}>
        <div style={{ fontSize: 13, fontWeight: 700, color: colors.stroke }}>{getLabel(score)}</div>
        <div style={{ fontSize: 12, color: "var(--text-muted)", marginTop: 2 }}>{label}</div>
      </div>
    </div>
  )
}

export function MiniScoreBar({ label, score, color = "#6366f1", delay = 0 }) {
  const [width, setWidth] = useState(0)
  useEffect(() => {
    const t = setTimeout(() => setWidth(score), 300 + delay)
    return () => clearTimeout(t)
  }, [score, delay])

  return (
    <div style={{ marginBottom: 14 }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
        <span style={{ fontSize: 13, color: "var(--text-secondary)", fontWeight: 500 }}>{label}</span>
        <span style={{ fontSize: 13, color, fontWeight: 700, fontFamily: "JetBrains Mono, monospace" }}>
          {Math.round(score)}%
        </span>
      </div>
      <div className="progress-bar">
        <div
          className="progress-fill"
          style={{ width: `${width}%`, background: `linear-gradient(90deg, ${color}aa, ${color})` }}
        />
      </div>
    </div>
  )
}
