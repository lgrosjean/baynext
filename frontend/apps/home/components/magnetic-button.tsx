"use client"

import { Button } from "@workspace/ui/components/button"
import { useRef, useState, type MouseEvent, type ReactNode } from "react"

interface MagneticButtonProps {
  children: ReactNode
  className?: string
  variant?: "default" | "outline" | "ghost"
  size?: "default" | "sm" | "lg"
  magneticStrength?: number
  onClick?: () => void
}

export function MagneticButton({
  children,
  className = "",
  variant = "default",
  size = "default",
  magneticStrength = 0.3,
  onClick,
}: MagneticButtonProps) {
  const buttonRef = useRef<HTMLButtonElement>(null)
  const [isHovered, setIsHovered] = useState(false)

  const handleMouseMove = (e: MouseEvent<HTMLButtonElement>) => {
    if (!buttonRef.current) return

    const button = buttonRef.current
    const rect = button.getBoundingClientRect()
    const centerX = rect.left + rect.width / 2
    const centerY = rect.top + rect.height / 2

    const deltaX = (e.clientX - centerX) * magneticStrength
    const deltaY = (e.clientY - centerY) * magneticStrength

    button.style.transform = `translate(${deltaX}px, ${deltaY}px) scale(${isHovered ? 1.05 : 1})`
  }

  const handleMouseEnter = () => {
    setIsHovered(true)
    if (buttonRef.current) {
      buttonRef.current.style.transition = "transform 0.2s ease-out"
    }
  }

  const handleMouseLeave = () => {
    setIsHovered(false)
    if (buttonRef.current) {
      buttonRef.current.style.transition = "transform 0.4s ease-out"
      buttonRef.current.style.transform = "translate(0px, 0px) scale(1)"
    }
  }

  return (
    <Button
      ref={buttonRef}
      variant={variant}
      size={size}
      className={`${className} cursor-pointer will-change-transform`}
      onMouseMove={handleMouseMove}
      onMouseEnter={handleMouseEnter}
      onMouseLeave={handleMouseLeave}
      onClick={onClick}
    >
      {children}
    </Button>
  )
}
