import { useState } from "react"
import { LandingHero } from "./components/LandingHero.jsx"
import { ResumeAnalyzer } from "./components/ResumeAnalyzer.jsx"
import { ResultsDashboard } from "./components/ResultsDashboard.jsx"
import { useScreening } from "./hooks/useScreening.js"

export default function App() {
  const [view, setView] = useState("landing") // landing | analyzer | results
  const screening = useScreening()

  const handleStart = () => {
    setView("analyzer")
  }

  const handleResult = (result) => {
    setView("results")
  }

  const handleReset = () => {
    screening.reset()
    setView("analyzer")
  }

  return (
    <>
      {view === "landing" && <LandingHero onStart={handleStart} />}
      {view === "analyzer" && <ResumeAnalyzer screening={screening} onResult={handleResult} />}
      {view === "results" && <ResultsDashboard result={screening.result} onReset={handleReset} />}
    </>
  )
}
