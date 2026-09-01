// API client for Resume Intelligence Platform backend
const BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"

export async function screenResume(file, jobDescription) {
  const formData = new FormData()
  formData.append("resume", file)
  formData.append("job_description", jobDescription)

  const response = await fetch(`${BASE_URL}/api/screen`, {
    method: "POST",
    body: formData,
  })

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: "Unknown server error" }))
    throw new Error(error.detail || `Server error: ${response.status}`)
  }

  return response.json()
}

export async function getTemplates() {
  const response = await fetch(`${BASE_URL}/api/templates`)
  if (!response.ok) throw new Error("Failed to load templates")
  return response.json()
}

export async function healthCheck() {
  const response = await fetch(`${BASE_URL}/api/health`)
  return response.ok
}
