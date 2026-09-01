import { useState, useRef, useCallback } from "react"

export function FileDropZone({ onFile, file }) {
  const [dragging, setDragging] = useState(false)
  const inputRef = useRef(null)

  const handleDrop = useCallback((e) => {
    e.preventDefault()
    setDragging(false)
    const dropped = e.dataTransfer.files[0]
    if (dropped && (dropped.name.endsWith(".pdf") || dropped.name.endsWith(".docx"))) {
      onFile(dropped)
    }
  }, [onFile])

  const handleChange = (e) => {
    const selected = e.target.files[0]
    if (selected) onFile(selected)
  }

  return (
    <div
      className={`dropzone ${dragging ? "active" : ""}`}
      style={{
        minHeight: 200, display: "flex", flexDirection: "column",
        alignItems: "center", justifyContent: "center",
        padding: 32, textAlign: "center", position: "relative"
      }}
      onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      onClick={() => !file && inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx"
        style={{ display: "none" }}
        onChange={handleChange}
      />
      {file ? (
        <div>
          <div style={{
            width: 60, height: 60, margin: "0 auto 16px",
            background: "rgba(16,185,129,0.15)", borderRadius: 14,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 28
          }}>📄</div>
          <div style={{ fontWeight: 700, fontSize: 15, color: "#10b981", marginBottom: 4 }}>
            {file.name}
          </div>
          <div style={{ fontSize: 12, color: "var(--text-muted)", marginBottom: 14 }}>
            {(file.size / 1024).toFixed(1)} KB
          </div>
          <button
            className="btn-secondary"
            style={{ fontSize: 12, padding: "7px 16px" }}
            onClick={(e) => { e.stopPropagation(); inputRef.current?.click() }}
          >
            Replace File
          </button>
        </div>
      ) : (
        <div>
          <div style={{
            width: 64, height: 64, margin: "0 auto 20px",
            background: dragging ? "rgba(99,102,241,0.2)" : "rgba(99,102,241,0.08)",
            border: "2px dashed rgba(99,102,241,0.4)",
            borderRadius: 16,
            display: "flex", alignItems: "center", justifyContent: "center",
            fontSize: 28, transition: "all 0.2s"
          }}>
            {dragging ? "✨" : "📥"}
          </div>
          <div style={{ fontWeight: 700, fontSize: 15, color: "var(--text-primary)", marginBottom: 8 }}>
            {dragging ? "Drop it here!" : "Drop your resume here"}
          </div>
          <div style={{ fontSize: 13, color: "var(--text-muted)", marginBottom: 16 }}>
            PDF · Max 10 MB
          </div>
          <button className="btn-secondary" style={{ fontSize: 13 }} onClick={(e) => { e.stopPropagation(); inputRef.current?.click() }}>
            Browse Files
          </button>
        </div>
      )}
    </div>
  )
}
