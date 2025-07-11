import Link from "next/link"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@workspace/ui/components/table"

import { ArrowUpRight } from "lucide-react";

import ms from 'ms';

import { PipelineWithDatasetNameAndJobs } from "@/actions/pipelines";


export const TemplatesTable = ({ pipelines }: {pipelines: PipelineWithDatasetNameAndJobs[]}) => {

    return (
        <Table>
            {/* <TableCaption>A list of your datasets.</TableCaption> */}
            <TableHeader>
                <TableRow className="bg-gray-100 hover:bg-gray-100">
                    <TableHead className="w-[200px]">Template</TableHead>
                    <TableHead className="w-[200px]">Dataset</TableHead>
                    <TableHead className="w-[100px]">Last job</TableHead>
                    <TableHead className="w-[100px]">Last updated</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {pipelines.map(({ pipeline, dataset, jobs }) => (

                    <TableRow key={pipeline.id}>
                        <TableCell>{pipeline.id}</TableCell>
                        <TableCell>
                            <Link href={`/app/projects/${pipeline.projectId}/datasets/${dataset.id}`}
                            className="text-neonBlue-600 hover:text-neonBlue-700 underline"
                            >
                                {dataset.name}
                                <ArrowUpRight className="inline-block ml-1" size={12} />
                            </Link>
                            </TableCell>
                        <TableCell>
                            {jobs.length > 0 && jobs[0] ? (
                                <Link href={`/app/projects/${pipeline.projectId}/jobs/${jobs[0]}`}
                                className="text-neonBlue-600 hover:text-neonBlue-700 underline"
                                >
                                    {jobs[0]}
                                    <ArrowUpRight className="inline-block ml-1" size={12} />
                                </Link>
                            ) : (
                                <span>-</span>
                            )}
                        </TableCell>
                        <TableCell>{ms(new Date().getTime() - pipeline.updatedAt.getTime())} ago</TableCell>
                    </TableRow>

                ))}
            </TableBody>
        </Table>
    )
}