"use client";

import { useParams } from 'next/navigation'
import { getProjectById } from '@/actions/projects';
import { getDataset } from '@/actions/datasets';

import { Slash, Table2, Folder } from "lucide-react"
import Image from "next/image";
import {
    Breadcrumb,
    BreadcrumbItem,
    BreadcrumbLink,
    BreadcrumbList,
    BreadcrumbSeparator,
} from "@workspace/ui/components/breadcrumb"

import { GeistMono } from 'geist/font/mono';
import { useState, useEffect } from 'react';

type Team = {
    name: string
    avatar? : string | null
}

function NavProject({ team }: {team: Team}) {

    return (
        <div className="flex items-center gap-2 p-2 rounded-sm hover:bg-radial hover:from-neonPurple-700 hover:to-neonPurple-900">
            {/* <div className="bg-linear-to-br from-neonBlue-500 to-neonPink-500 text-neonPurple-900  flex aspect-square size-5 items-center justify-center rounded-sm">
                <Command className="size-3" />
            </div> */}
            <div className="grid flex-1 text-left text-sm leading-tight text-white">
                <span className={`${GeistMono.className} truncate font-medium`}>{team.name}</span>
            </div>
        </div>
    )
}

export function NavProjects({ team }: { team: Team }) {

    const params = useParams<{ projectId: string; datasetId: string }>()

    const [projectName, setProjectName] = useState<string | null>(null);
    const [datasetName, setDatasetName] = useState<string | null>(null);

    useEffect(() => {
        if (params.projectId) {
            getProjectById(params.projectId)
                .then((project) => {
                    setProjectName(project.name);
                })
                .catch((error) => {
                    console.error("Error fetching project name:", error);
                });
        }
        else {
            setProjectName(null);
        }
        if (params.datasetId) {
            getDataset(params.projectId, params.datasetId)
                .then((dataset) => {
                    setDatasetName(dataset.name);
                })
                .catch((error) => {
                    console.error("Error fetching dataset name:", error);
                });
        }
        else {
            setDatasetName(null);
        }
    }
    , [params.projectId, params.datasetId]);


    return (
        <Breadcrumb className="hidden sm:block">
            <BreadcrumbList>
                <BreadcrumbItem>
                    <BreadcrumbLink href="/app">
                        <Image src="/apple-touch-icon.png" alt="Logo" width={180} height={180} className="rounded-full size-12" />
                    </BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator>
                    <Slash size={16} />
                </BreadcrumbSeparator>
                <BreadcrumbItem>
                    <BreadcrumbLink href="/app/projects">
                        <NavProject team={team} />
                    </BreadcrumbLink>
                </BreadcrumbItem>
                {projectName && (
                    <>
                        <BreadcrumbSeparator>
                            <Slash />
                        </BreadcrumbSeparator>
                        <BreadcrumbItem className='gap-0 text-primary-foreground'>
                            <Folder size={16} strokeWidth={2} />
                            <BreadcrumbLink href={`/app/projects/${params.projectId}`}>
                                <NavProject team={{name: projectName}} />
                            </BreadcrumbLink>
                        </BreadcrumbItem>
                    </>
                )}
                {datasetName && (
                    <>
                        <BreadcrumbSeparator>
                            <Slash />
                        </BreadcrumbSeparator>
                        <BreadcrumbItem className='gap-0 text-primary-foreground'>
                            <Table2 size={16} strokeWidth={2} />
                            <BreadcrumbLink href={`/app/projects/${params.projectId}/datasets/${params.datasetId}`}>
                                <NavProject team={{name: datasetName}} />
                            </BreadcrumbLink>
                        </BreadcrumbItem>
                    </>
                )}
            </BreadcrumbList>
        </Breadcrumb>
    )
}