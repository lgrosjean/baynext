"use client"

import { Card, CardDescription, CardHeader, CardTitle } from "@workspace/ui/components/card";
import { useIntersectionObserver } from "@/hooks/use-intersection-observer"
import type { ReactNode } from "react"

interface AnimatedCardProps {
  icon: ReactNode
  title: string
  description: string
  borderColor: string
  iconGradient: string
  shadowColor: string
  delay?: number
}

export function AnimatedCard({
  icon,
  title,
  description,
  borderColor,
  iconGradient,
  shadowColor,
  delay = 0,
}: AnimatedCardProps) {
  const { ref, isIntersecting } = useIntersectionObserver({
    threshold: 0.2,
    rootMargin: "-50px",
  })

  return (
    <div
      ref={ref}
      className={`transform transition-all duration-700 ease-out ${
        isIntersecting ? "translate-y-0 opacity-100" : "translate-y-8 opacity-0"
      }`}
      style={{
        transitionDelay: `${delay}ms`,
      }}
    >
      <Card
        className={`bg-gradient-to-br from-gray-900/50 to-gray-800/50 ${borderColor} hover:border-opacity-40 transition-all duration-300 group hover:shadow-lg ${shadowColor}`}
      >
        <CardHeader>
          <div
            className={`w-12 h-12 bg-gradient-to-r ${iconGradient} rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}
          >
            {icon}
          </div>
          <CardTitle className="text-xl text-white">{title}</CardTitle>
          <CardDescription className="text-gray-400">{description}</CardDescription>
        </CardHeader>
      </Card>
    </div>
  )
}
