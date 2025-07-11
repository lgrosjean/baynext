import Link from "next/link"
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@workspace/ui/components/table"

import { Dataset } from "@/types/datasets"

import { ArrowUpRight } from "lucide-react";

export const DatasetsTable = ({ datasets }: { datasets: Dataset[] }) => {
    

    return (
        <Table>
            <TableHeader>
                <TableRow>
                    <TableHead className="w-[100px]">Name</TableHead>
                    <TableHead className="w-[100px]">ID</TableHead>
                    <TableHead className="w-[100px]">Last edited</TableHead>
                </TableRow>
            </TableHeader>
            <TableBody>
                {datasets.map((dataset) => (

                    <TableRow key={dataset.id}>
                        <TableCell>
                            <Link href={`/app/projects/${dataset.projectId}/datasets/${dataset.id}`}
                            className="text-neonBlue-600 hover:text-neonBlue-700 underline"
                            >
                                {dataset.name}
                                <ArrowUpRight className="inline-block ml-1" size={12} />    
                            </Link>
                        </TableCell>
                        <TableCell>{dataset.id}</TableCell>
                        <TableCell>{dataset.uploadedAt?.toLocaleDateString()}</TableCell>
                    </TableRow>

                ))}
            </TableBody>
        </Table>
    )
}