import Link from "next/link"
import { GalleryVerticalEnd } from "lucide-react"
import Image from "next/image"
import { LoginForm } from "@/components/login/login-form"

export default function LoginPage() {
  return (
    <div className="grid min-h-svh lg:grid-cols-2 bg-gradient-to-br from-tertiary via-tertiary to-primary">
      <div className="flex flex-col gap-4 p-6 md:p-10">
      <div className="flex justify-center gap-2 md:justify-start">
        <Link href="#" className="flex items-center gap-2 font-medium text-primary-foreground">
        <div className="bg-primary flex size-6 items-center justify-center rounded-md">
          <GalleryVerticalEnd className="size-4" />
        </div>
        BayNext
        </Link>
      </div>
      <div className="flex flex-1 items-center justify-center">
        <div className="w-full max-w-xs">
        <LoginForm />
        </div>
      </div>
      </div>
      <div className="bg-muted relative hidden lg:block">
      <Image
        src="/home.png"
        alt="Image"
        fill
        className="absolute inset-0 h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
      />
      </div>
    </div>
  )
}
