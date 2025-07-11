"use client"

import { useScroll } from "@/hooks/use-scroll"

export function ParallaxBackground() {
  const { scrollY } = useScroll()

  return (
    <div className="fixed inset-0 pointer-events-none overflow-hidden">
      {/* Layer 1 - Slowest moving background elements */}
      <div
        className="absolute inset-0"
        style={{
          transform: `translateY(${scrollY * 0.1}px)`,
        }}
      >
        <div className="absolute top-[10%] left-[5%] w-96 h-96 bg-cyan-500/5 rounded-full blur-3xl" />
        <div className="absolute top-[60%] right-[10%] w-80 h-80 bg-purple-500/5 rounded-full blur-3xl" />
        <div className="absolute bottom-[20%] left-[20%] w-64 h-64 bg-green-500/5 rounded-full blur-3xl" />
      </div>

      {/* Layer 2 - Medium speed elements */}
      <div
        className="absolute inset-0"
        style={{
          transform: `translateY(${scrollY * 0.2}px)`,
        }}
      >
        <div className="absolute top-[30%] right-[5%] w-48 h-48 bg-cyan-400/10 rounded-full blur-2xl animate-pulse" />
        <div className="absolute top-[80%] left-[10%] w-56 h-56 bg-purple-400/10 rounded-full blur-2xl animate-pulse delay-1000" />
        <div className="absolute top-[50%] left-[50%] w-32 h-32 bg-yellow-400/10 rounded-full blur-2xl animate-pulse delay-500" />
      </div>

      {/* Layer 3 - Faster moving elements */}
      <div
        className="absolute inset-0"
        style={{
          transform: `translateY(${scrollY * 0.3}px)`,
        }}
      >
        <div className="absolute top-[20%] left-[70%] w-24 h-24 bg-cyan-300/15 rounded-full blur-xl" />
        <div className="absolute top-[70%] right-[20%] w-28 h-28 bg-purple-300/15 rounded-full blur-xl" />
        <div className="absolute bottom-[40%] left-[40%] w-20 h-20 bg-pink-300/15 rounded-full blur-xl" />
      </div>

      {/* Layer 4 - Floating geometric shapes */}
      <div
        className="absolute inset-0"
        style={{
          transform: `translateY(${scrollY * 0.15}px) rotate(${scrollY * 0.05}deg)`,
        }}
      >
        <div className="absolute top-[25%] left-[15%] w-4 h-4 bg-gradient-to-r from-cyan-400/30 to-purple-400/30 rotate-45 blur-sm" />
        <div className="absolute top-[65%] right-[25%] w-6 h-6 bg-gradient-to-r from-purple-400/30 to-pink-400/30 rotate-12 blur-sm" />
        <div className="absolute bottom-[30%] left-[60%] w-3 h-3 bg-gradient-to-r from-green-400/30 to-blue-400/30 rotate-45 blur-sm" />
      </div>

      {/* Layer 5 - Grid pattern overlay */}
      <div
        className="absolute inset-0 opacity-5"
        style={{
          transform: `translateY(${scrollY * 0.05}px)`,
          backgroundImage: `
            linear-gradient(rgba(6, 182, 212, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(6, 182, 212, 0.1) 1px, transparent 1px)
          `,
          backgroundSize: "100px 100px",
        }}
      />
    </div>
  )
}
