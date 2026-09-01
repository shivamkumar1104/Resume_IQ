import { useState } from "react"
import { FileDropZone } from "./ui/FileDropZone.jsx"
import { ProgressSteps } from "./ui/ProgressSteps.jsx"

const JD_PLACEHOLDER = `Paste the job description here...

Example:
We are looking for a Senior Full Stack Engineer with 4+ years of experience building scalable web applications using React.js, Node.js, and PostgreSQL. Strong knowledge of REST APIs, Docker, AWS, and CI/CD pipelines required. Experience with TypeScript, Redis, and system design a plus.`

export function ResumeAnalyzer({ onResult, screening }) {
  const [file, setFile] = useState(null)
  const [jd, setJd] = useState("")
  const [charCount, setCharCount] = useState(0)

  const handleJdChange = (e) => {
    setJd(e.target.value)
    setCharCount(e.target.value.length)
  }

  const handleSubmit = async () => {
    if (!file || !jd.trim()) return
    const result = await screening.screen(file, jd)
    if (result) onResult(result)
  }

  const isLoading = screening.status === "loading"
  const canSubmit = file && jd.trim().length >= 50 && !isLoading

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column" }}>
      {/* Header bar */}
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "space-between",
        padding: "18px 40px",
        background: "rgba(6,9,19,0.8)", backdropFilter: "blur(20px)",
        borderBottom: "1px solid rgba(255,255,255,0.05)"
      }}>
        <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
          <div style={{
            width: 32, height: 32, borderRadius: 9,
            background: "linear-gradient(135deg, #6366f1, #06b6d4)",
            display: "flex", alignItems: "center", justifyContent: "center", fontSize: 15
          }}>🎯</div>
          <span style={{ fontWeight: 800, fontSize: 15 }}>ResumeIQ</span>
        </div>
        <button className="btn-secondary" style={{ fontSize: 12, padding: "7px 16px" }} onClick={() => screening.reset()}>
          ← Back
        </button>
      </div>

      {isLoading ? (
        /* ── Loading State ── */
        <div style={{
          flex: 1, display: "flex", flexDirection: "column",
          alignItems: "center", justifyContent: "center", padding: 40
        }}>
          <div style={{
            width: 80, height: 80, borderRadius: 22, marginBottom: 32,
            background: "linear-gradient(135deg, rgba(99,102,241,0.2), rgba(6,182,212,0.1))",
            border: "2px solid rgba(99,102,241,0.3)",
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 36, animation: "pulse-dot 2s ease-in-out infinite"
          }}>
            🧠
          </div>
          <h2 style={{ fontWeight: 800, fontSize: 24, marginBottom: 8, letterSpacing: "-0.02em" }}>
            Analyzing Resume
          </h2>
          <p style={{ color: "var(--text-muted)", fontSize: 14, marginBottom: 48 }}>
            Running AI intelligence pipeline…
          </p>
          <ProgressSteps
            steps={screening.steps}
            currentStep={screening.currentStep}
            progress={screening.progress}
          />
        </div>
      ) : (
        /* ── Input Form ── */
        <div style={{
          flex: 1, maxWidth: 1200, width: "100%",
          margin: "0 auto", padding: "48px 32px"
        }}>
          <div style={{ marginBottom: 40, textAlign: "center" }}>
            <h1 style={{ fontSize: 32, fontWeight: 800, letterSpacing: "-0.03em", marginBottom: 10 }}>
              Analyze a <span className="gradient-text">Candidate</span>
            </h1>
            <p style={{ color: "var(--text-muted)", fontSize: 15 }}>
              Upload a resume and paste the job description to get a full intelligence report
            </p>
          </div>

          <div style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: 28, marginBottom: 32
          }}>
            {/* Left: Upload */}
            <div>
              <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 14 }}>
                <div className="section-label">Resume Upload</div>
                <span style={{ fontSize: 11, color: "var(--accent-primary)", fontWeight: 600 }}>PDF · DOCX</span>
              </div>
              <FileDropZone file={file} onFile={setFile} />
            </div>

            {/* Right: JD */}
            <div>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14 }}>
                <div className="section-label">Job Description</div>
                <span style={{
                  fontSize: 11, color: charCount < 50 ? "var(--accent-rose)" : "var(--text-muted)",
                  fontFamily: "JetBrains Mono, monospace"
                }}>
                  {charCount} chars {charCount < 50 ? "(min 50)" : "✓"}
                </span>
              </div>
              <textarea
                className="input-field"
                style={{ height: 200, lineHeight: 1.65 }}
                placeholder={JD_PLACEHOLDER}
                value={jd}
                onChange={handleJdChange}
              />
            </div>
          </div>

          {/* Checklist */}
          <div style={{
            display: "flex", gap: 24, marginBottom: 32, flexWrap: "wrap",
            padding: "16px 20px",
            background: "rgba(255,255,255,0.02)", borderRadius: 12,
            border: "1px solid rgba(255,255,255,0.05)"
          }}>
            {[
              { ok: !!file, label: "Resume uploaded" },
              { ok: charCount >= 50, label: "JD entered (50+ chars)" },
            ].map((item, i) => (
              <div key={i} style={{ display: "flex", alignItems: "center", gap: 8 }}>
                <span style={{ fontSize: 14 }}>{item.ok ? "✅" : "⬜"}</span>
                <span style={{ fontSize: 13, color: item.ok ? "#10b981" : "var(--text-muted)" }}>
                  {item.label}
                </span>
              </div>
            ))}
          </div>

          {/* Error */}
          {screening.error && (
            <div style={{
              marginBottom: 24, padding: "14px 18px", borderRadius: 10,
              background: "rgba(244,63,94,0.1)", border: "1px solid rgba(244,63,94,0.3)",
              color: "#fb7185", fontSize: 14
            }}>
              ⚠️ {screening.error}
            </div>
          )}

          {/* Submit */}
          <div style={{ display: "flex", justifyContent: "center" }}>
            <button
              className="btn-primary"
              style={{
                fontSize: 16, padding: "16px 56px",
                opacity: canSubmit ? 1 : 0.4,
                cursor: canSubmit ? "pointer" : "not-allowed",
                pointerEvents: canSubmit ? "auto" : "none"
              }}
              onClick={handleSubmit}
              disabled={!canSubmit}
            >
              🚀 Run Intelligence Analysis
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
