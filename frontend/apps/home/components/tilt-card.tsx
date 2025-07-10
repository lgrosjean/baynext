"use client"

import { Card, CardDescription, CardHeader, CardTitle } from "@workspace/ui/components/card"
import { useIntersectionObserver } from "@/hooks/use-intersection-observer"
import { useRef, useState, type MouseEvent, type ReactNode } from "react"

interface TiltCardProps {
  icon: ReactNode
  title: string
  description: string
  borderColor: string
  iconGradient: string
  shadowColor: string
  delay?: number
  tiltStrength?: number
}

export function TiltCard({
  icon,
  title,
  description,
  borderColor,
  iconGradient,
  shadowColor,
  delay = 0,
  tiltStrength = 15,
}: TiltCardProps) {
  const { ref: intersectionRef, isIntersecting } = useIntersectionObserver({
    threshold: 0.2,
    rootMargin: "-50px",
  })

  const cardRef = useRef<HTMLDivElement>(null)
  const [isHovered, setIsHovered] = useState(false)

  const handleMouseMove = (e: MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return

    const card = cardRef.current
    const rect = card.getBoundingClientRect()
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 2

    const rotateX = ((e.clientY - centerY) / rect.height) * -tiltStrength
    const rotateY = ((e.clientX - centerX) / rect.width) * tiltStrength

    card.style.transform = `
      perspective(1000px) 
      rotateX(${rotateX}deg) 
      rotateY(${rotateY}deg) 
      scale3d(${isHovered ? 1.05 : 1}, ${isHovered ? 1.05 : 1}, ${isHovered ? 1.05 : 1})
      translateZ(${isHovered ? 20 : 0}px)
    `
  }

  const handleMouseEnter = () => {
    setIsHovered(true)
    if (cardRef.current) {
      cardRef.current.style.transition = "transform 0.1s ease-out"
    }
  }

  const handleMouseLeave = () => {
    setIsHovered(false)
    if (cardRef.current) {
      cardRef.current.style.transition = "transform 0.5s ease-out"
      cardRef.current.style.transform = `
        perspective(1000px) 
        rotateX(0deg) 
        rotateY(0deg) 
        scale3d(1, 1, 1)
        translateZ(0px)
      `
    }
  }

  return (
    <div
      ref={intersectionRef}
      className={`transform transition-all duration-700 ease-out ${
        isIntersecting ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0"
      }`}
      style={{
        transitionDelay: `${delay}ms`,
      }}
    >
      <div
        ref={cardRef}
        className="will-change-transform"
        onMouseMove={handleMouseMove}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
      >
        <Card
          className={`bg-gradient-to-br from-gray-900/50 to-gray-800/50 ${borderColor} hover:border-opacity-40 transition-all duration-300 group hover:shadow-lg ${shadowColor} relative overflow-hidden`}
        >
          {/* Shine effect overlay */}
          <div
            className={`absolute inset-0 opacity-0 group-hover:opacity-20 transition-opacity duration-300 pointer-events-none ${
              isHovered ? "bg-gradient-to-br from-white/10 via-transparent to-transparent" : ""
            }`}
          />

          {/* Glow effect */}
          <div
            className={`absolute inset-0 opacity-0 group-hover:opacity-30 transition-opacity duration-300 pointer-events-none blur-xl ${
              iconGradient.includes("cyan")
                ? "bg-cyan-500/20"
                : iconGradient.includes("purple")
                  ? "bg-purple-500/20"
                  : iconGradient.includes("green")
                    ? "bg-green-500/20"
                    : iconGradient.includes("yellow")
                      ? "bg-yellow-500/20"
                      : iconGradient.includes("pink")
                        ? "bg-pink-500/20"
                        : "bg-blue-500/20"
            }`}
          />

          <CardHeader className="relative z-10">
            <div
              className={`w-12 h-12 bg-gradient-to-r ${iconGradient} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300 shadow-lg`}
              style={{
                transform: isHovered ? "translateZ(10px)" : "translateZ(0px)",
                transition: "transform 0.3s ease-out",
              }}
            >
              {icon}
            </div>
            <CardTitle
              className="text-xl text-white transition-transform duration-300"
              style={{
                transform: isHovered ? "translateZ(5px)" : "translateZ(0px)",
              }}
            >
              {title}
            </CardTitle>
            <CardDescription
              className="text-gray-400 transition-transform duration-300"
              style={{
                transform: isHovered ? "translateZ(3px)" : "translateZ(0px)",
              }}
            >
              {description}
            </CardDescription>
          </CardHeader>

          {/* Floating particles effect */}
          <div className="absolute inset-0 pointer-events-none overflow-hidden">
            {isHovered && (
              <>
                <div
                  className="absolute w-1 h-1 bg-cyan-400/60 rounded-full animate-ping"
                  style={{
                    top: "20%",
                    left: "80%",
                    animationDelay: "0ms",
                    animationDuration: "2s",
                  }}
                />
                <div
                  className="absolute w-1 h-1 bg-purple-400/60 rounded-full animate-ping"
                  style={{
                    top: "70%",
                    left: "20%",
                    animationDelay: "500ms",
                    animationDuration: "2s",
                  }}
                />
                <div
                  className="absolute w-0.5 h-0.5 bg-white/40 rounded-full animate-ping"
                  style={{
                    top: "40%",
                    left: "60%",
                    animationDelay: "1000ms",
                    animationDuration: "2s",
                  }}
                />
              </>
            )}
          </div>
        </Card>
      </div>
    </div>
  )
}
