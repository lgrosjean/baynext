import { NewModelForm } from "@/components/projects/models/new-model-form";

export default async function NewModeltPage({
    params,
    searchParams,
}: {
    params: Promise<{ projectId: string }>,
    searchParams?: Promise<{
        datasetId?: string,
    }>
}) {

    const { projectId } = await params;
    const { datasetId } = await searchParams || {};

    return (
        <section>
            <div className="mb-10">
                <h1 className="text-2xl">Create a new model</h1>
            </div>

            <NewModelForm projectId={projectId} datasetId={datasetId} />

        </section>
    );
}