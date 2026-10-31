import { useEffect, useRef, useState } from "react"
import { BASE_URL } from "../utils/api.js"

function AnimatedCounter({ target, suffix = "", duration = 2000 }) {
  const [value, setValue] = useState(0)
  const ref = useRef(null)
  useEffect(() => {
    const observer = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        let start = null
        const animate = (ts) => {
          if (!start) start = ts
          const p = Math.min((ts - start) / duration, 1)
          const eased = 1 - Math.pow(1 - p, 3)
          setValue(Math.round(eased * target))
          if (p < 1) requestAnimationFrame(animate)
        }
        requestAnimationFrame(animate)
        observer.disconnect()
      }
    })
    if (ref.current) observer.observe(ref.current)
    return () => observer.disconnect()
  }, [target, duration])
  return <span ref={ref}>{value.toLocaleString()}{suffix}</span>
}

const FEATURES = [
  { icon: "🧠", title: "Universal Skill Extraction", desc: "No whitelists. Detects modern, niche, and emerging tech terms with grounded evidence." },
  { icon: "📊", title: "Explainable Match Scoring", desc: "Blueprint-weighted formula: Skills 40% + Experience 25% + Projects 20% + Education 5% + Semantic 10%." },
  { icon: "🔍", title: "Full ATS Diagnostics", desc: "7-point compliance check: sections, action verbs, quantification, keywords, length, and formatting." },
  { icon: "✍️", title: "AI Improvement Engine", desc: "Grounded suggestions using Google X-Y-Z formula — zero hallucination, 100% candidate-verified." },
  { icon: "📋", title: "Company Template Engine", desc: "Recruiter screening summaries, interview checklists, and shortlist memos — ready to deploy." },
  { icon: "⚡", title: "Real-time Processing", desc: "Full analysis pipeline completes in under 3 seconds with SentenceTransformer semantic matching." },
]

const STATS = [
  { value: 95, suffix: "%", label: "ATS Compatibility Rate" },
  { value: 3,  suffix: "s", label: "Avg. Analysis Time" },
  { value: 7,  suffix: "", label: "ATS Diagnostic Checks" },
  { value: 40, suffix: "+", label: "Skill Categories" },
]

export function LandingHero({ onStart }) {
  return (
    <div style={{ minHeight: "100vh", position: "relative", overflow: "hidden" }}>
      {/* Ambient background blobs */}
      <div style={{
        position: "fixed", top: -200, left: -200, width: 700, height: 700,
        borderRadius: "50%",
        background: "radial-gradient(circle, rgba(99,102,241,0.12) 0%, transparent 70%)",
        animation: "float1 18s ease-in-out infinite",
        pointerEvents: "none", zIndex: 0
      }} />
      <div style={{
        position: "fixed", bottom: -200, right: -100, width: 600, height: 600,
        borderRadius: "50%",
        background: "radial-gradient(circle, rgba(6,182,212,0.10) 0%, transparent 70%)",
        animation: "float2 22s ease-in-out infinite",
        pointerEvents: "none", zIndex: 0
      }} />

      {/* Nav */}
      <nav style={{
        position: "fixed", top: 0, left: 0, right: 0, zIndex: 50,
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "18px 48px",
        background: "rgba(6,9,19,0.8)",
        backdropFilter: "blur(20px)",
        borderBottom: "1px solid rgba(255,255,255,0.05)"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 34, height: 34, borderRadius: 10,
            background: "linear-gradient(135deg, #6366f1, #06b6d4)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 16
          }}>🎯</div>
          <span style={{ fontWeight: 800, fontSize: 16, letterSpacing: "-0.02em" }}>ResumeIQ</span>
        </div>
        <div style={{ display: "flex", gap: 8 }}>
          <button className="btn-secondary" style={{ fontSize: 13, padding: "8px 18px" }} onClick={() => window.open(`${BASE_URL}/api/docs`, "_blank")}>
            API Docs
          </button>
          <button className="btn-primary" style={{ fontSize: 13, padding: "9px 20px" }} onClick={onStart}>
            Try Now →
          </button>
        </div>
      </nav>

      {/* Hero */}
      <section style={{
        maxWidth: 900, margin: "0 auto",
        paddingTop: 160, paddingBottom: 80, paddingLeft: 24, paddingRight: 24,
        textAlign: "center", position: "relative", zIndex: 1
      }}>
        {/* Pill badge */}
        <div className="fade-in-up" style={{
          display: "inline-flex", alignItems: "center", gap: 8, marginBottom: 32,
          padding: "7px 18px", borderRadius: 20,
          background: "rgba(99,102,241,0.12)", border: "1px solid rgba(99,102,241,0.3)"
        }}>
          <span style={{ fontSize: 10, fontWeight: 800, color: "#a5b4fc", textTransform: "uppercase", letterSpacing: "0.1em" }}>
            Enterprise AI Platform
          </span>
          <span style={{ fontSize: 10, color: "var(--text-muted)" }}>v3.0</span>
        </div>

        <h1 className="fade-in-up fade-in-up-d1" style={{
          fontSize: "clamp(42px, 7vw, 76px)",
          fontWeight: 900, lineHeight: 1.05,
          letterSpacing: "-0.03em", marginBottom: 24
        }}>
          <span className="gradient-text">Resume Intelligence</span>
          <br />
          <span style={{ color: "var(--text-primary)" }}>Beyond Keyword Matching</span>
        </h1>

        <p className="fade-in-up fade-in-up-d2" style={{
          fontSize: 18, color: "var(--text-secondary)", lineHeight: 1.7,
          maxWidth: 620, margin: "0 auto 48px", fontWeight: 400
        }}>
          Enterprise-grade AI that dynamically extracts skills, computes explainable match scores,
          runs full ATS diagnostics, and generates company-ready hiring templates.
        </p>

        <div className="fade-in-up fade-in-up-d3" style={{ display: "flex", gap: 16, justifyContent: "center", flexWrap: "wrap" }}>
          <button className="btn-primary" style={{ fontSize: 16, padding: "16px 40px" }} onClick={onStart}>
            🚀 Analyze a Resume
          </button>
          <button className="btn-secondary" style={{ fontSize: 15, padding: "15px 30px" }} onClick={() => window.open(`${BASE_URL}/api/docs`, "_blank")}>
            View API Docs
          </button>
        </div>

        {/* Stats row */}
        <div className="fade-in-up fade-in-up-d4" style={{
          display: "grid", gridTemplateColumns: "repeat(4, 1fr)",
          gap: 1, marginTop: 80,
          background: "rgba(255,255,255,0.04)", borderRadius: 16,
          border: "1px solid rgba(255,255,255,0.06)", overflow: "hidden"
        }}>
          {STATS.map((s, i) => (
            <div key={i} style={{
              padding: "28px 20px", textAlign: "center",
              background: "rgba(0,0,0,0.2)",
              borderRight: i < STATS.length - 1 ? "1px solid rgba(255,255,255,0.05)" : "none"
            }}>
              <div className="stat-value gradient-text">
                <AnimatedCounter target={s.value} suffix={s.suffix} />
              </div>
              <div style={{ fontSize: 12, color: "var(--text-muted)", marginTop: 6, fontWeight: 500 }}>
                {s.label}
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Features grid */}
      <section style={{
        maxWidth: 1100, margin: "0 auto",
        padding: "80px 24px", position: "relative", zIndex: 1
      }}>
        <div style={{ textAlign: "center", marginBottom: 56 }}>
          <div className="section-label" style={{ marginBottom: 12 }}>What It Does</div>
          <h2 style={{ fontSize: "clamp(28px, 4vw, 40px)", fontWeight: 800, letterSpacing: "-0.02em" }}>
            Every Layer of Intelligence
          </h2>
        </div>
        <div style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(300px, 1fr))",
          gap: 20
        }}>
          {FEATURES.map((f, i) => (
            <div key={i} className={`card fade-in-up`} style={{
              padding: 28, animationDelay: `${i * 0.07}s`
            }}>
              <div style={{
                width: 50, height: 50, borderRadius: 14, marginBottom: 18,
                background: "rgba(99,102,241,0.1)", border: "1px solid rgba(99,102,241,0.2)",
                display: "flex", alignItems: "center", justifyContent: "center", fontSize: 24
              }}>{f.icon}</div>
              <div style={{ fontWeight: 700, fontSize: 16, marginBottom: 10 }}>{f.title}</div>
              <div style={{ fontSize: 14, color: "var(--text-secondary)", lineHeight: 1.65 }}>{f.desc}</div>
            </div>
          ))}
        </div>
      </section>

      {/* CTA Banner */}
      <section style={{
        maxWidth: 800, margin: "0 auto 100px",
        padding: "0 24px", textAlign: "center", position: "relative", zIndex: 1
      }}>
        <div style={{
          padding: "52px 48px", borderRadius: 24,
          background: "linear-gradient(135deg, rgba(99,102,241,0.15), rgba(6,182,212,0.1))",
          border: "1px solid rgba(99,102,241,0.25)"
        }}>
          <h2 style={{ fontSize: 32, fontWeight: 800, marginBottom: 16, letterSpacing: "-0.02em" }}>
            Ready to screen smarter?
          </h2>
          <p style={{ fontSize: 16, color: "var(--text-secondary)", marginBottom: 32 }}>
            Upload any PDF resume and get a full intelligence report in seconds.
          </p>
          <button className="btn-primary" style={{ fontSize: 16, padding: "16px 44px" }} onClick={onStart}>
            Start Analysis →
          </button>
        </div>
      </section>
    </div>
  )
}
