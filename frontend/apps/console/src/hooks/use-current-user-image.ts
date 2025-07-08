"use client";
import { auth } from "@/auth"
import { useSession } from "next-auth/react"
import { useState, useEffect } from "react"

export const useCurrentUserImage = async () => {
    const [image, setImage] = useState<string | null>(null)

    useEffect(() => {
        const fetchUser = async () => {
            const session = await auth()
            setImage(session?.user.image ?? null)
        }
        fetchUser()
    }, [])

    return image
}
    