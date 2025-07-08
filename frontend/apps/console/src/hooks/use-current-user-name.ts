"use client";

import { useSession } from "next-auth/react"
import { useEffect, useState } from 'react'

export const useCurrentUserName = () => {
  const [name, setName] = useState<string | null>(null)

  useEffect(() => {
    const fetchProfileName = async () => {
        const { data: session } = useSession()
        setName(session?.user.name ?? null)
    }
    fetchProfileName()
  }, [])

  return name
}