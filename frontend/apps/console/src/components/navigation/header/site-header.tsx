import { auth } from "@/auth"


import { NavProjects } from "./nav-project-breadcrumb"
import { NavUser } from "./nav-user"

export async function SiteHeader() {

    const user = (await auth())?.user

    const project = {
        team: {
            name: user!.name || "Project",
            avatar: user?.image || null,
        }
    }

    return (
        <header className="flex bg-neonPurple-900 fixed top-0 z-50 w-full items-center">
            <div className="flex h-header-height w-full items-center gap-2 px-6">

                <NavProjects team={project.team} />

                <div className="flex items-center gap-3 ml-auto">
                    <NavUser user={user} />
                </div>
            </div>
        </header>
    )
}
