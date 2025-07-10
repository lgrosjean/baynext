import type { Metadata } from 'next'

import "@workspace/ui/globals.css"
import '@/styles/globals.css'


export const metadata: Metadata = {
  title: 'Baynext',
  description: 'Baynext is a next-generation platform for building, training and analyzing MMM models with ease.',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
