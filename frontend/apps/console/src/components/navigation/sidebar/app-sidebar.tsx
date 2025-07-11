"use client"

import { useParams } from 'next/navigation'

import * as React from "react"
import {
  GalleryVerticalEnd,
  Settings2,
  LayoutDashboard,
  Table2,
  Box,
  TrendingUpDown,
  Route,
  ChartArea,
} from "lucide-react"

import { NavMain } from "@/components/navigation/sidebar/nav-main"
import { NavProject } from "@/components/navigation/sidebar/nav-projects"

import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
} from "@workspace/ui/components/sidebar"


const navAccount = [
  {
    title: "Overview",
    url: "/app/projects",
    icon: GalleryVerticalEnd,
    isActive: true,
  },
  {
    title: "Settings",
    url: "/app/settings",
    icon: Settings2,
  },
]


export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {

  const { projectId } = useParams<{ projectId: string }>()

  const navProject = [
    {
      title: "Performance",
      url: `/app/projects/${projectId}/performance`,
      icon: ChartArea,
    },
    {
      title: "Scenarios",
      url: `/app/projects/${projectId}/scenarios`,
      icon: TrendingUpDown,
    },
  ]

  const navEditor = [
    {
      title: "Dashboard",
      url: `/app/projects/${projectId}`,
      icon: LayoutDashboard,
      // isActive: true,
    },
    {
      title: "Datasets",
      url: `/app/projects/${projectId}/datasets`,
      icon: Table2,
    },
    {
      title: "Pipelines",
      url: `/app/projects/${projectId}/pipelines`,
      icon: Route,
    },
    {
      title: "Models",
      url: `/app/projects/${projectId}/models`,
      icon: Box,
    },
    {
      title: "Settings",
      url: `/app/projects/${projectId}/settings`,
      icon: Settings2,
    },
  ]

  return (
    <Sidebar
      className="top-(--header-height) !h-[calc(100svh-var(--header-height))]"
      {...props}
    >
      <SidebarHeader>
      </SidebarHeader>

      <SidebarContent>
        
        {projectId ?
        <>
          <NavProject items={navProject} />
          <NavProject items={navEditor} />
        </> : <NavMain items={navAccount} />
        }
      </SidebarContent>
      <SidebarFooter>
      </SidebarFooter>
    </Sidebar>
  )
}
