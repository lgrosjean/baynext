import { NewDatasetForm } from "@/components/projects/datasets/new-dataset-form";

export default async function NewDatasetPage({ params }: { params: Promise<{ projectId: string }>}) {
    const { projectId } = await params;
    
    return (
        <section>
        <div className="mb-8">
            <h1 className="text-2xl">New Dataset</h1>
            <p>Upload and configure your dataset here.</p>
        </div>
    
        <div>

            <NewDatasetForm projectId={projectId} />
        </div>
        </section>
    );
    }