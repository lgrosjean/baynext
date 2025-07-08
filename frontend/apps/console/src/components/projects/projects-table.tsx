"use client"

import { useRouter } from 'next/navigation'

import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@workspace/ui/components/table"


type Project = {
    id: string
    userId: string
    name: string
    description?: string
    createdAt: Date
    updatedAt?: Date
}

export const ProjectsTable = ({ projects }: { projects: Project[] }) => {
    const router = useRouter()

    return (
        <Table>
            {/* <TableCaption>A list of your projects.</TableCaption> */}
            <TableHeader>
                <TableRow>
                    <TableHead className="w-[100px]">Name</TableHead>
                    <TableHead className="w-[100px]">Description</TableHead>
                    {/* <TableHead className="w-[100px]">Created at</TableHead> */}
                    <TableHead className="w-[100px]">Last edited</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {projects.map((project) => (

                    <TableRow key={project.id} onClick={() => { router.push(`/app/projects/${project.id}`) }} className="cursor-pointer">
                        <TableCell>{project.name}</TableCell>
                        <TableCell>{project.description}</TableCell>
                        {/* <TableCell>{project.createdAt.toLocaleDateString()}</TableCell> */}
                        <TableCell>{project.updatedAt?.toLocaleDateString()}</TableCell>
                    </TableRow>

                ))}
            </TableBody>
        </Table>
    )
}