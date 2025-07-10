"use client"

import { Zap } from "lucide-react"
import { useEffect, useState } from "react"

interface LoadingScreenProps {
  onLoadingComplete: () => void
}

export function LoadingScreen({ onLoadingComplete }: LoadingScreenProps) {
  const [progress, setProgress] = useState(0)
  const [loadingText, setLoadingText] = useState("Initializing")
  const [isExiting, setIsExiting] = useState(false)

  const loadingSteps = [
    { text: "Initializing", duration: 800 },
    { text: "Loading MMM Engine", duration: 600 },
    { text: "Connecting Analytics", duration: 500 },
    { text: "Preparing Dashboard", duration: 400 },
    { text: "Almost Ready", duration: 300 },
  ]

  useEffect(() => {
    let currentStep = 0
    let currentProgress = 0

    const updateProgress = () => {
      if (currentStep < loadingSteps.length) {
        const step = loadingSteps[currentStep]
        setLoadingText(step.text)

        const stepProgress = 100 / loadingSteps.length
        const targetProgress = (currentStep + 1) * stepProgress

        const progressInterval = setInterval(() => {
          currentProgress += 2
          setProgress(Math.min(currentProgress, targetProgress))

          if (currentProgress >= targetProgress) {
            clearInterval(progressInterval)
            currentStep++

            if (currentStep < loadingSteps.length) {
              setTimeout(updateProgress, 100)
            } else {
              // Complete loading
              setTimeout(() => {
                setProgress(100)
                setLoadingText("Ready!")
                setTimeout(() => {
                  setIsExiting(true)
                  setTimeout(onLoadingComplete, 800)
                }, 500)
              }, 200)
            }
          }
        }, 30)
      }
    }

    const initialDelay = setTimeout(updateProgress, 500)

    return () => {
      clearTimeout(initialDelay)
    }
  }, [onLoadingComplete])

  return (
    <div
      className={`fixed inset-0 z-[9999] bg-black flex items-center justify-center transition-all duration-800 ease-in-out ${
        isExiting ? "opacity-0 scale-110" : "opacity-100 scale-100"
      }`}
    >
      {/* Animated Background */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse" />
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000" />
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-cyan-500/5 to-purple-500/5 rounded-full blur-3xl animate-spin-slow" />
      </div>

      {/* Loading Content */}
      <div className="relative z-10 text-center">
        {/* Logo Animation */}
        <div className="mb-8 flex justify-center">
          <div className="relative">
            <div className="w-20 h-20 bg-gradient-to-r from-cyan-400 to-purple-500 rounded-2xl flex items-center justify-center animate-pulse">
              <Zap className="w-10 h-10 text-black animate-bounce" />
            </div>

            {/* Rotating Ring */}
            <div className="absolute inset-0 border-2 border-transparent border-t-cyan-400 border-r-purple-500 rounded-2xl animate-spin" />

            {/* Outer Glow Ring */}
            <div className="absolute -inset-2 border border-cyan-400/30 rounded-3xl animate-ping" />
          </div>
        </div>

        {/* Brand Name */}
        <h1 className="text-4xl font-bold mb-8 bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent animate-gradient">
          Baynext
        </h1>

        {/* Progress Bar Container */}
        <div className="w-80 mx-auto mb-6">
          <div className="relative h-2 bg-gray-800 rounded-full overflow-hidden">
            {/* Background Glow */}
            <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-full" />

            {/* Progress Fill */}
            <div
              className="absolute top-0 left-0 h-full bg-gradient-to-r from-cyan-400 to-purple-500 rounded-full transition-all duration-300 ease-out shadow-lg shadow-cyan-500/50"
              style={{ width: `${progress}%` }}
            />

            {/* Animated Shine Effect */}
            <div
              className="absolute top-0 h-full w-8 bg-gradient-to-r from-transparent via-white/30 to-transparent skew-x-12 animate-pulse"
              style={{
                left: `${Math.max(0, progress - 10)}%`,
                transition: "left 0.3s ease-out",
              }}
            />
          </div>

          {/* Progress Percentage */}
          <div className="flex justify-between items-center mt-2 text-sm">
            <span className="text-gray-400">{Math.round(progress)}%</span>
            <span className="text-cyan-400 font-medium">{loadingText}</span>
          </div>
        </div>

        {/* Loading Dots Animation */}
        <div className="flex justify-center space-x-2 mb-8">
          <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
          <div className="w-2 h-2 bg-purple-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
          <div className="w-2 h-2 bg-cyan-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
        </div>

        {/* Floating Particles */}
        <div className="absolute inset-0 pointer-events-none">
          <div
            className="absolute top-1/4 left-1/3 w-1 h-1 bg-cyan-400/60 rounded-full animate-ping"
            style={{ animationDelay: "0s" }}
          />
          <div
            className="absolute top-1/3 right-1/4 w-1 h-1 bg-purple-400/60 rounded-full animate-ping"
            style={{ animationDelay: "1s" }}
          />
          <div
            className="absolute bottom-1/3 left-1/4 w-1 h-1 bg-cyan-400/60 rounded-full animate-ping"
            style={{ animationDelay: "2s" }}
          />
          <div
            className="absolute bottom-1/4 right-1/3 w-1 h-1 bg-purple-400/60 rounded-full animate-ping"
            style={{ animationDelay: "0.5s" }}
          />
          <div
            className="absolute top-1/2 left-1/5 w-0.5 h-0.5 bg-white/40 rounded-full animate-ping"
            style={{ animationDelay: "1.5s" }}
          />
          <div
            className="absolute top-3/4 right-1/5 w-0.5 h-0.5 bg-white/40 rounded-full animate-ping"
            style={{ animationDelay: "2.5s" }}
          />
        </div>

        {/* Tagline */}
        <p className="text-gray-400 text-sm animate-pulse">Revolutionizing Marketing Mix Modeling</p>
      </div>

      {/* Scan Line Effect */}
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-cyan-400/50 to-transparent animate-scan-line" />
      </div>
    </div>
  )
}
