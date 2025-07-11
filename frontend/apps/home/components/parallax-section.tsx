"use client"

import { useScroll } from "@/hooks/use-scroll"
import type { ReactNode } from "react"

interface ParallaxSectionProps {
  children: ReactNode
  className?: string
  speed?: number
  id?: string
}

export function ParallaxSection({ children, className = "", speed = 0.1, id }: ParallaxSectionProps) {
  const { scrollY } = useScroll()

  return (
    <section
      id={id}
      className={`relative ${className}`}
      style={{
        transform: `translateY(${scrollY * speed}px)`,
      }}
    >
      {children}
    </section>
  )
}
