import "@workspace/ui/globals.css"

import type { Metadata } from "next";

import { GeistSans } from 'geist/font/sans';

export const metadata: Metadata = {
    title: "Baynext Console",
};

export default async function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    
    return (
        <html lang="en" className={`${GeistSans.className} antialiased`} suppressHydrationWarning>
            <body>
                {children}
            </body>
        </html >
    );
}
