import {
    Table,
    TableBody,
    TableCaption,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@workspace/ui/components/table"

import ms from 'ms';

import { 
    Ban,
    CircleCheck,
    CircleDashed,
    LoaderCircle,
 } from "lucide-react"

import { JobWithPipeline, JobStatus } from "@/types"

const statusIcons = {
    [JobStatus.Pending]: <CircleDashed className="text-yellow-500 size-4" />,
    [JobStatus.Running]: <LoaderCircle className="text-blue-500 size-4" />,
    [JobStatus.Completed]: <CircleCheck className="text-green-500 size-4" />,
    [JobStatus.Failed]: <Ban className="text-red-500 size-4" />,
}


export const JobsTable = ({ jobs }: {jobs: JobWithPipeline[]}) => {

    return (
        <Table>
            {/* <TableCaption>A list of your datasets.</TableCaption> */}
            <TableHeader>
                <TableRow>
                    <TableHead className="w-[5px]"></TableHead>
                    <TableHead className="w-[100px]">Job</TableHead>
                    <TableHead className="w-[100px]">Template</TableHead>
                    <TableHead className="w-[100px]">Duration</TableHead>
                    <TableHead className="w-[100px]">Started at</TableHead>
                    <TableHead className="w-[100px]">Finished at</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {jobs.map(({job, pipeline}) => (

                    <TableRow key={job.id}>
                        <TableCell>{statusIcons[job.status]}</TableCell>
                        <TableCell>{job.id}</TableCell>
                        <TableCell>{pipeline.id}</TableCell>
                        <TableCell>{job.finishedAt && job.startedAt ? ms(job.finishedAt.getTime() - job.startedAt.getTime()) : 0}</TableCell>
                        <TableCell>{job.startedAt?.toLocaleDateString()} {job.startedAt?.toLocaleTimeString()}</TableCell>
                        <TableCell>{job.finishedAt?.toLocaleDateString()}</TableCell>
                    </TableRow>

                ))}
            </TableBody>
        </Table>
    )
}