"use client"

import { MagneticButton } from "@/components/magnetic-button"
import { TiltCard } from "@/components/tilt-card"
import { ParallaxHero } from "@/components/parallax-hero"
import { ParallaxBackground } from "@/components/parallax-background"
import { ParallaxSection } from "@/components/parallax-section"
import { LoadingScreen } from "@/components/loading-screen"
import { BarChart3, Database, TrendingUp, Zap, ArrowRight, Users, Shield } from "lucide-react"
import Link from "next/link"
import { useState } from "react"

export default function LandingPage() {
  const [isLoading, setIsLoading] = useState(true)

  const handleLoadingComplete = () => {
    setIsLoading(false)
  }

  if (isLoading) {
    return <LoadingScreen onLoadingComplete={handleLoadingComplete} />
  }

  return (
    <div className="min-h-screen bg-black text-white overflow-hidden relative">
      {/* Global Parallax Background */}
      <ParallaxBackground />

      {/* Header */}
      <header className="relative z-50 border-b border-cyan-500/20 bg-black/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-cyan-400 to-purple-500 rounded-lg flex items-center justify-center">
              <Zap className="w-5 h-5 text-black" />
            </div>
            <span className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
              Baynext
            </span>
          </div>
          <nav className="hidden md:flex items-center space-x-8">
            <Link href="#features" className="text-gray-300 hover:text-cyan-400 transition-colors">
              Features
            </Link>
            <Link href="#pricing" className="text-gray-300 hover:text-cyan-400 transition-colors">
              Pricing
            </Link>
            <Link href="#about" className="text-gray-300 hover:text-cyan-400 transition-colors">
              About
            </Link>
          </nav>
          <div className="flex items-center space-x-4">
            <MagneticButton
              variant="ghost"
              magneticStrength={0.2}
              className="text-cyan-400 hover:text-cyan-300 hover:bg-cyan-400/10"
            >
              Login
            </MagneticButton>
            <MagneticButton
              magneticStrength={0.3}
              className="bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-600 hover:to-purple-700 text-white border-0 shadow-lg shadow-cyan-500/25"
            >
              Sign Up
            </MagneticButton>
          </div>
        </div>
      </header>

      {/* Hero Section with Parallax */}
      <ParallaxHero />

      {/* Features Section with Parallax */}
      <ParallaxSection id="features" className="py-20 relative z-10" speed={0.05}>
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-4">
              <span className="bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
                Powerful Features
              </span>
            </h2>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              Tools designed to help you master Mix Marketing Model operations
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            <TiltCard
              icon={<BarChart3 className="w-6 h-6 text-white" />}
              title="Simplified MMM Training"
              description="Streamline your model training process with automated pipelines and intelligent preprocessing"
              borderColor="border-cyan-500/20"
              iconGradient="from-cyan-500 to-cyan-600"
              shadowColor="hover:shadow-cyan-500/10"
              delay={0}
              tiltStrength={12}
            />

            <TiltCard
              icon={<Database className="w-6 h-6 text-white" />}
              title="Dataset Versioning"
              description="Track, manage, and version your datasets with enterprise-grade data lineage and governance"
              borderColor="border-purple-500/20"
              iconGradient="from-purple-500 to-purple-600"
              shadowColor="hover:shadow-purple-500/10"
              delay={100}
              tiltStrength={12}
            />

            <TiltCard
              icon={<TrendingUp className="w-6 h-6 text-white" />}
              title="ROI Analysis"
              description="Deep-dive into model outputs with interactive dashboards and comprehensive ROI insights"
              borderColor="border-green-500/20"
              iconGradient="from-green-500 to-green-600"
              shadowColor="hover:shadow-green-500/10"
              delay={200}
              tiltStrength={12}
            />

            <TiltCard
              icon={<Zap className="w-6 h-6 text-white" />}
              title="Budget Optimization"
              description="Optimize your marketing spend with AI-powered recommendations and scenario planning"
              borderColor="border-yellow-500/20"
              iconGradient="from-yellow-500 to-yellow-600"
              shadowColor="hover:shadow-yellow-500/10"
              delay={300}
              tiltStrength={12}
            />

            <TiltCard
              icon={<Users className="w-6 h-6 text-white" />}
              title="Team Collaboration"
              description="Built for seamless teamwork with shared workspaces and collaboration features"
              borderColor="border-pink-500/20"
              iconGradient="from-pink-500 to-pink-600"
              shadowColor="hover:shadow-pink-500/10"
              delay={400}
              tiltStrength={12}
            />

            <TiltCard
              icon={<Shield className="w-6 h-6 text-white" />}
              title="Enterprise Security"
              description="Designed with security in mind, featuring modern authentication and access controls"
              orde
              rColor="border-blue-500/20"
              iconGradient="from-blue-500 to-blue-600"
              shadowColor="hover:shadow-blue-500/10"
              delay={500}
              tiltStrength={12}
            />
          </div>
        </div>
      </ParallaxSection>

      {/* CTA Section with Parallax */}
      <ParallaxSection className="py-20 relative z-10" speed={0.03}>
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 to-purple-500/10"></div>
        <div className="container mx-auto px-4 relative z-10">
          <div className="text-center max-w-3xl mx-auto">
            <h2 className="text-4xl md:text-5xl font-bold mb-6">
              <span className="bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">
                Ready to Streamline Your
              </span>
              <br />
              <span className="bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
                Marketing Operations?
              </span>
            </h2>
            <p className="text-xl text-gray-300 mb-8">
              Discover how Baynext can help optimize your marketing mix modeling workflow
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <MagneticButton
                size="lg"
                magneticStrength={0.4}
                className="bg-gradient-to-r from-cyan-500 to-purple-600 hover:from-cyan-600 hover:to-purple-700 text-white px-8 py-4 text-lg font-semibold shadow-lg shadow-cyan-500/25 hover:shadow-cyan-500/40 transition-all duration-300 group border-0"
              >
                Access Console
                <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </MagneticButton>
              <MagneticButton
                size="lg"
                variant="outline"
                magneticStrength={0.3}
                className="border-purple-500/50 text-purple-400 hover:bg-purple-500/10 px-8 py-4 text-lg font-semibold bg-transparent"
              >
                Schedule Demo
              </MagneticButton>
            </div>
          </div>
        </div>
      </ParallaxSection>

      {/* Footer */}
      <footer className="border-t border-gray-800 py-12 relative z-10">
        <div className="container mx-auto px-4">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="w-8 h-8 bg-gradient-to-r from-cyan-400 to-purple-500 rounded-lg flex items-center justify-center">
                <Zap className="w-5 h-5 text-black" />
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
                Baynext
              </span>
            </div>
            <div className="flex space-x-6 text-gray-400">
              <Link href="#" className="hover:text-cyan-400 transition-colors">
                Privacy
              </Link>
              <Link href="#" className="hover:text-cyan-400 transition-colors">
                Terms
              </Link>
              <Link href="#" className="hover:text-cyan-400 transition-colors">
                Support
              </Link>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-800 text-center text-gray-500">
            <p>&copy; 2024 Baynext. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}
