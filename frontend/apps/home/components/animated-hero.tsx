"use client"

import { MagneticButton } from "@/components/magnetic-button"
import { ArrowRight, Play } from "lucide-react"
import { useEffect, useState } from "react"

export function AnimatedHero() {
  const [isLoaded, setIsLoaded] = useState(false)

  useEffect(() => {
    // Trigger animations after component mounts
    const timer = setTimeout(() => {
      setIsLoaded(true)
    }, 100)

    return () => clearTimeout(timer)
  }, [])

  return (
    <section className="relative py-20 md:py-32 overflow-hidden">
      {/* Animated Background */}
      <div className="absolute inset-0">
        <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-cyan-500/5 to-purple-500/5 rounded-full blur-3xl animate-spin-slow"></div>
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div className="text-center max-w-4xl mx-auto">
          {/* Badge Animation */}
          <div
            className={`inline-block mb-6 px-4 py-2 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-full border border-cyan-500/30 transform transition-all duration-1000 ease-out ${
              isLoaded ? "translate-y-0 opacity-100 scale-100" : "translate-y-4 opacity-0 scale-95"
            }`}
            style={{ transitionDelay: "200ms" }}
          >
            <span className="text-cyan-400 text-sm font-medium">🚀 Revolutionize Your Marketing Mix Modeling</span>
          </div>

          {/* Main Title Animation */}
          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
            <span
              className={`block bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent animate-gradient transform transition-all duration-1000 ease-out ${
                isLoaded ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0"
              }`}
              style={{ transitionDelay: "400ms" }}
            >
              Operationalize
            </span>
            <span
              className={`block bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent transform transition-all duration-1000 ease-out ${
                isLoaded ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0"
              }`}
              style={{ transitionDelay: "600ms" }}
            >
              MMM at Scale
            </span>
          </h1>

          {/* Description Animation */}
          <p
            className={`text-xl md:text-2xl text-gray-300 mb-8 leading-relaxed transform transition-all duration-1000 ease-out ${
              isLoaded ? "translate-y-0 opacity-100" : "translate-y-6 opacity-0"
            }`}
            style={{ transitionDelay: "800ms" }}
          >
            A platform designed to simplify MMM training, manage dataset versions, and help analyze marketing ROI with
            modern tools for data-driven marketers.
          </p>

          {/* Magnetic Buttons Animation */}
          <div
            className={`flex flex-col sm:flex-row gap-4 justify-center items-center mb-12 transform transition-all duration-1000 ease-out ${
              isLoaded ? "translate-y-0 opacity-100" : "translate-y-6 opacity-0"
            }`}
            style={{ transitionDelay: "1000ms" }}
          >
            <MagneticButton
              size="lg"
              magneticStrength={0.4}
              className="bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-600 hover:to-purple-700 text-white px-8 py-4 text-lg font-semibold shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 transition-all duration-300 group border-0"
            >
              Start Free Trial
              <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </MagneticButton>

            <MagneticButton
              size="lg"
              variant="outline"
              magneticStrength={0.3}
              className="border-cyan-500/50 text-cyan-400 hover:bg-cyan-500/10 px-8 py-4 text-lg font-semibold group bg-transparent"
            >
              <Play className="mr-2 w-5 h-5 group-hover:scale-110 transition-transform" />
              Watch Demo
            </MagneticButton>
          </div>

          {/* Floating Elements Animation */}
          <div className="relative">
            {/* Floating Icon 1 */}
            <div
              className={`absolute -top-20 -left-20 w-16 h-16 bg-gradient-to-r from-cyan-400/20 to-purple-500/20 rounded-full flex items-center justify-center backdrop-blur-sm border border-cyan-500/30 transform transition-all duration-1500 ease-out ${
                isLoaded ? "translate-y-0 opacity-100 rotate-0" : "translate-y-8 opacity-0 rotate-45"
              }`}
              style={{ transitionDelay: "1200ms" }}
            >
              <div className="w-6 h-6 bg-gradient-to-r from-cyan-400 to-purple-500 rounded-full animate-pulse"></div>
            </div>

            {/* Floating Icon 2 */}
            <div
              className={`absolute -top-16 -right-16 w-12 h-12 bg-gradient-to-r from-purple-400/20 to-cyan-500/20 rounded-full flex items-center justify-center backdrop-blur-sm border border-purple-500/30 transform transition-all duration-1500 ease-out ${
                isLoaded ? "translate-y-0 opacity-100 rotate-0" : "translate-y-6 opacity-0 -rotate-45"
              }`}
              style={{ transitionDelay: "1400ms" }}
            >
              <div className="w-4 h-4 bg-gradient-to-r from-purple-400 to-cyan-500 rounded-full animate-pulse delay-500"></div>
            </div>

            {/* Floating Icon 3 */}
            <div
              className={`absolute -bottom-10 left-10 w-10 h-10 bg-gradient-to-r from-green-400/20 to-blue-500/20 rounded-full flex items-center justify-center backdrop-blur-sm border border-green-500/30 transform transition-all duration-1500 ease-out ${
                isLoaded ? "translate-y-0 opacity-100 rotate-0" : "translate-y-4 opacity-0 rotate-90"
              }`}
              style={{ transitionDelay: "1600ms" }}
            >
              <div className="w-3 h-3 bg-gradient-to-r from-green-400 to-blue-500 rounded-full animate-pulse delay-1000"></div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
