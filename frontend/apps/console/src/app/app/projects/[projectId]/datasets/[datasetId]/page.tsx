import Link from "next/link";
import { getDataset, getDatasetMetadata } from "@/actions/datasets";
import { DatasetDropdownMenu } from "@/components/projects/datasets/dataset-dropdown-menu";
import { Button } from "@workspace/ui/components/button";

import { Undo2 } from "lucide-react";

export default async function DatasetPage({ params }: { params: Promise<{ projectId: string, datasetId: string }> }) {

    const { projectId, datasetId } = await params;

    const dataset = await getDataset(projectId, datasetId);

    if (!dataset) {
        return <div>Dataset not found</div>;
    }

    const datasetMetadata = await getDatasetMetadata(projectId, datasetId);

    return (
        <section>
            <div className="flex items-start justify-between mb-4">
                <div className="flex items-center gap-2">
                    <Link href={`/app/projects/${projectId}/datasets`}>
                        <Undo2 className="size-6 text-neonBlue-600 hover:text-neonBlue-700 rounded-sm hover:bg-gray-100 p-1" />
                    </Link>
                <h1 className="text-2xl">{dataset.name}</h1>
                </div>
                <div className="flex ml-auto gap-2">
                    <Link href={`/app/projects/${projectId}/models/new?datasetId=${datasetId}`}>
                        <Button variant="default" className="w-full">
                            Create a model
                        </Button>
                    </Link>
                    <DatasetDropdownMenu dataset={dataset} />
                </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 border rounded-md shadow-sm bg-white">
                <span className="text-sm font-semibold">Dataset size</span>
                <p className="text-sm text-gray-500">
                    {datasetMetadata.size > 1e6
                        ? `${(datasetMetadata.size / 1e6).toFixed(2)} MB`
                        : datasetMetadata.size > 1000
                        ? `${(datasetMetadata.size / 1000).toFixed(2)} KB`
                        : `${datasetMetadata.size} bytes`}
                </p>
            </div>
            <div className="p-4 border rounded-md shadow-sm bg-white">
                <h2 className="text-lg font-semibold mb-2">Created on</h2>
                <p className="text-sm text-gray-500">
                    {new Date(dataset.uploadedAt).toLocaleDateString("en-US", {
                        year: "numeric",
                        month: "long",
                        day: "numeric",
                        hour: "2-digit",
                        minute: "2-digit",
                    })}
                </p>
            </div>
            </div>
        </section>
    );
}