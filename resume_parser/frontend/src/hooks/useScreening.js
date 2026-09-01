import { useState, useCallback } from "react"
import { screenResume } from "../utils/api.js"

const STEPS = [
  { id: "extract",  label: "Extracting Text",      icon: "📄" },
  { id: "skills",   label: "Analyzing Skills",      icon: "🧠" },
  { id: "scoring",  label: "Computing Scores",      icon: "📊" },
  { id: "ats",      label: "Running ATS Diagnostics", icon: "🔍" },
  { id: "complete", label: "Generating Report",     icon: "✨" },
]

export function useScreening() {
  const [status, setStatus] = useState("idle") // idle | loading | success | error
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [currentStep, setCurrentStep] = useState(0)
  const [progress, setProgress] = useState(0)

  const screen = useCallback(async (file, jobDescription) => {
    setStatus("loading")
    setResult(null)
    setError(null)
    setCurrentStep(0)
    setProgress(0)

    // Simulate step-by-step progress while request is in flight
    const stepDurations = [600, 800, 700, 600, 400]
    let stepIndex = 0

    const advanceStep = () => {
      if (stepIndex < STEPS.length - 1) {
        stepIndex++
        setCurrentStep(stepIndex)
        setProgress(Math.round((stepIndex / (STEPS.length - 1)) * 90))
        if (stepIndex < STEPS.length - 1) {
          setTimeout(advanceStep, stepDurations[stepIndex])
        }
      }
    }

    const timer = setTimeout(advanceStep, stepDurations[0])

    try {
      const data = await screenResume(file, jobDescription)
      clearTimeout(timer)
      setCurrentStep(STEPS.length - 1)
      setProgress(100)
      // Short delay to show 100% before showing results
      await new Promise(r => setTimeout(r, 400))
      setResult(data)
      setStatus("success")
    } catch (err) {
      clearTimeout(timer)
      setError(err.message || "An unexpected error occurred.")
      setStatus("error")
    }
  }, [])

  const reset = useCallback(() => {
    setStatus("idle")
    setResult(null)
    setError(null)
    setCurrentStep(0)
    setProgress(0)
  }, [])

  return { status, result, error, currentStep, progress, steps: STEPS, screen, reset }
}
