import "@workspace/ui/globals.css"
import { Toaster } from "@workspace/ui/components/sonner"

import type { Metadata } from "next";

import { GeistSans } from 'geist/font/sans';

export const metadata: Metadata = {
  title: "Baynext",
  description: "Marketing Modeling Platform powered by OSS & Cloud",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={GeistSans.className}>
      <body className="bg-tertiary">
        {children}
        <Toaster position="bottom-right" richColors />
      </body>
    </html>
  );
}
