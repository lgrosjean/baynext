"use client"

import { Button } from "@workspace/ui/components/button";
import { RefreshCw } from "lucide-react";

import { refreshDatasetsPage } from "@/actions/datasets";

export function RefreshButton({projectId }: {projectId: string}) {

    const onClick = async () => {
        await refreshDatasetsPage(projectId);
    }

    return (
        <Button
            onClick={onClick}
            variant="outline" size="icon">
            <RefreshCw className="h-4 w-4" />
        </Button>
    )
}