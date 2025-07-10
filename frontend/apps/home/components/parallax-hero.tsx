"use client"

import { MagneticButton } from "@/components/magnetic-button"
import { useScroll } from "@/hooks/use-scroll"
import { ArrowRight, Play } from "lucide-react"
import { useEffect, useState } from "react"

export function ParallaxHero() {
  const [isLoaded, setIsLoaded] = useState(false)
  const { scrollY } = useScroll()

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoaded(true)
    }, 100)

    return () => clearTimeout(timer)
  }, [])

  return (
    <section className="relative py-20 md:py-32 overflow-hidden min-h-screen flex items-center">
      {/* Parallax Background Elements */}
      <div className="absolute inset-0">
        {/* Main background orbs with parallax */}
        <div
          className="absolute top-1/4 left-1/4 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl animate-pulse"
          style={{
            transform: `translateY(${scrollY * 0.3}px) scale(${1 + scrollY * 0.0001})`,
          }}
        />
        <div
          className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-500/10 rounded-full blur-3xl animate-pulse delay-1000"
          style={{
            transform: `translateY(${scrollY * 0.4}px) scale(${1 + scrollY * 0.0001})`,
          }}
        />

        {/* Large rotating background */}
        <div
          className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-gradient-to-r from-cyan-500/5 to-purple-500/5 rounded-full blur-3xl"
          style={{
            transform: `
              translate(-50%, -50%) 
              translateY(${scrollY * 0.2}px) 
              rotate(${scrollY * 0.1}deg) 
              scale(${1 + scrollY * 0.0002})
            `,
          }}
        />

        {/* Additional floating elements */}
        <div
          className="absolute top-[10%] right-[10%] w-32 h-32 bg-gradient-to-r from-cyan-400/20 to-purple-400/20 rounded-full blur-xl"
          style={{
            transform: `translateY(${scrollY * 0.5}px) rotate(${scrollY * 0.2}deg)`,
          }}
        />
        <div
          className="absolute bottom-[10%] left-[10%] w-24 h-24 bg-gradient-to-r from-purple-400/20 to-pink-400/20 rounded-full blur-xl"
          style={{
            transform: `translateY(${scrollY * 0.6}px) rotate(${-scrollY * 0.15}deg)`,
          }}
        />
      </div>

      <div className="container mx-auto px-4 relative z-10">
        <div
          className="text-center max-w-4xl mx-auto"
          style={{
            transform: `translateY(${scrollY * 0.1}px)`,
          }}
        >
          {/* Badge Animation */}
          <div
            className={`inline-block mb-6 px-4 py-2 bg-gradient-to-r from-cyan-500/20 to-purple-500/20 rounded-full border border-cyan-500/30 transform transition-all duration-1000 ease-out ${
              isLoaded ? "translate-y-0 opacity-100 scale-100" : "translate-y-4 opacity-0 scale-95"
            }`}
            style={{
              transitionDelay: "200ms",
              transform: `translateY(${scrollY * 0.05}px) ${isLoaded ? "translateY(0)" : "translateY(16px)"} scale(${isLoaded ? 1 : 0.95})`,
            }}
          >
            <span className="text-cyan-400 text-sm font-medium">🚀 Revolutionize Your Marketing Mix Modeling</span>
          </div>

          {/* Main Title Animation with Parallax */}
          <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
            <span
              className={`block bg-gradient-to-r from-white via-cyan-200 to-purple-300 bg-clip-text text-transparent animate-gradient transform transition-all duration-1000 ease-out ${
                isLoaded ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0"
              }`}
              style={{
                transitionDelay: "400ms",
                transform: `translateY(${scrollY * 0.08}px) ${isLoaded ? "translateY(0)" : "translateY(32px)"}`,
              }}
            >
              Operationalize
            </span>
            <span
              className={`block bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent transform transition-all duration-1000 ease-out ${
                isLoaded ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0"
              }`}
              style={{
                transitionDelay: "600ms",
                transform: `translateY(${scrollY * 0.12}px) ${isLoaded ? "translateY(0)" : "translateY(32px)"}`,
              }}
            >
              MMM at Scale
            </span>
          </h1>

          {/* Description with Parallax */}
          <p
            className={`text-xl md:text-2xl text-gray-300 mb-8 leading-relaxed transform transition-all duration-1000 ease-out ${
              isLoaded ? "translate-y-0 opacity-100" : "translate-y-6 opacity-0"
            }`}
            style={{
              transitionDelay: "800ms",
              transform: `translateY(${scrollY * 0.06}px) ${isLoaded ? "translateY(0)" : "translateY(24px)"}`,
            }}
          >
            A platform designed to simplify MMM training, manage dataset versions, and help analyze marketing ROI with
            modern tools for data-driven marketers.
          </p>

          {/* Buttons with Parallax */}
          <div
            className={`flex flex-col sm:flex-row gap-4 justify-center items-center mb-12 transform transition-all duration-1000 ease-out ${
              isLoaded ? "translate-y-0 opacity-100" : "translate-y-6 opacity-0"
            }`}
            style={{
              transitionDelay: "1000ms",
              transform: `translateY(${scrollY * 0.04}px) ${isLoaded ? "translateY(0)" : "translateY(24px)"}`,
            }}
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

          {/* Floating Elements with Enhanced Parallax */}
          <div className="relative">
            <div
              className={`absolute -top-20 -left-20 w-16 h-16 bg-gradient-to-r from-cyan-400/20 to-purple-500/20 rounded-full flex items-center justify-center backdrop-blur-sm border border-cyan-500/30 transform transition-all duration-1500 ease-out ${
                isLoaded ? "translate-y-0 opacity-100 rotate-0" : "translate-y-8 opacity-0 rotate-45"
              }`}
              style={{
                transitionDelay: "1200ms",
                transform: `translateY(${scrollY * 0.7}px) rotate(${scrollY * 0.3}deg) ${isLoaded ? "translateY(0) rotate(0deg)" : "translateY(32px) rotate(45deg)"}`,
              }}
            >
              <div className="w-6 h-6 bg-gradient-to-r from-cyan-400 to-purple-500 rounded-full animate-pulse"></div>
            </div>

            <div
              className={`absolute -top-16 -right-16 w-12 h-12 bg-gradient-to-r from-purple-400/20 to-cyan-500/20 rounded-full flex items-center justify-center backdrop-blur-sm border border-purple-500/30 transform transition-all duration-1500 ease-out ${
                isLoaded ? "translate-y-0 opacity-100 rotate-0" : "translate-y-6 opacity-0 -rotate-45"
              }`}
              style={{
                transitionDelay: "1400ms",
                transform: `translateY(${scrollY * 0.8}px) rotate(${-scrollY * 0.2}deg) ${isLoaded ? "translateY(0) rotate(0deg)" : "translateY(24px) rotate(-45deg)"}`,
              }}
            >
              <div className="w-4 h-4 bg-gradient-to-r from-purple-400 to-cyan-500 rounded-full animate-pulse delay-500"></div>
            </div>

            <div
              className={`absolute -bottom-10 left-10 w-10 h-10 bg-gradient-to-r from-green-400/20 to-blue-500/20 rounded-full flex items-center justify-center backdrop-blur-sm border border-green-500/30 transform transition-all duration-1500 ease-out ${
                isLoaded ? "translate-y-0 opacity-100 rotate-0" : "translate-y-4 opacity-0 rotate-90"
              }`}
              style={{
                transitionDelay: "1600ms",
                transform: `translateY(${scrollY * 0.9}px) rotate(${scrollY * 0.4}deg) ${isLoaded ? "translateY(0) rotate(0deg)" : "translateY(16px) rotate(90deg)"}`,
              }}
            >
              <div className="w-3 h-3 bg-gradient-to-r from-green-400 to-blue-500 rounded-full animate-pulse delay-1000"></div>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
