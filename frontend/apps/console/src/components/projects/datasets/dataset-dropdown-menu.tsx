import { Button } from "@workspace/ui/components/button";
import {
    DropdownMenu,
    DropdownMenuTrigger,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuSeparator,

} from "@workspace/ui/components/dropdown-menu";
import {
    EllipsisVertical,
    Pencil,
} from "lucide-react";

import { DeleteDatasetMenuItem } from "./delete-dataset-menu-item"
import { Dataset } from "@/types/datasets"

export async function DatasetDropdownMenu({ dataset }: { dataset: Dataset }) {
    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="outline" className="ml-auto cursor-pointer" size="icon">
                    <EllipsisVertical />
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
                <DropdownMenuItem>
                    <Pencil />
                    Edit
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DeleteDatasetMenuItem dataset={dataset} />
            </DropdownMenuContent>
        </DropdownMenu>
    )
}