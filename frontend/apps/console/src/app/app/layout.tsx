import { Toaster } from "@workspace/ui/components/sonner"
import { SessionProvider } from "next-auth/react"

import { SidebarInset, SidebarProvider } from "@workspace/ui/components/sidebar"
import { AppSidebar } from "@/components/navigation/sidebar/app-sidebar"

import { SiteHeader } from "@/components/navigation/header/site-header"

export default async function Layout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {


    return (
        <SessionProvider>
            <SiteHeader />
            <SidebarProvider className="flex flex-col">
                <div className="flex flex-1 top-(--header-height) h-[calc(100svh-var(--header-height))]!">
                    <AppSidebar />
                    <SidebarInset className="top-(--header-height) !h-[calc(100svh-var(--header-height))]">
                        <main className="p-8">
                            {children}
                        </main>
                    </SidebarInset>

                </div>
            </SidebarProvider>
            <Toaster position="bottom-right" richColors />
        </SessionProvider>
    );
}
