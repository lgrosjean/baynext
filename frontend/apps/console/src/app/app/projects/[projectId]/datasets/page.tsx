import Link from "next/link";
import { getDatasets } from "@/actions/datasets";
import { EmptyProjectCard } from "@/components/projects/empty-project-card";

import { DatasetsTable } from "@/components/projects/datasets/datasets-table";
import { Button } from "@workspace/ui/components/button";

import { RefreshButton } from "@/components/projects/datasets/refresh-button";

export default async function DatasetsPage({ params }: { params: Promise<{ projectId: string }> }) {

    const { projectId } = await params;

    const datasets = await getDatasets(projectId);

    return (
        <section>
            <div className="flex items-start mb-4">
                <h1 className="text-2xl">My datasets</h1>
                <div className="flex ml-auto gap-2">
                    <Link href={`/app/projects/${projectId}/datasets/new`}>
                        {datasets.length > 0 && <Button variant="default" className="w-full">
                            Create a dataset
                        </Button>}
                    </Link>
                    <RefreshButton projectId={projectId} />

                </div>
            </div>

            <div>
                <p className="text-sm text-muted-foreground mb-8">
                    Datasets are the foundation of your projects. They are used to train and evaluate your MMM models.
                </p>
                
                {datasets.length === 0 ? (
                    <EmptyProjectCard projectId={projectId} />
                ) :
                    <DatasetsTable datasets={datasets} />
                }
            </div>

        </section>
    );
}