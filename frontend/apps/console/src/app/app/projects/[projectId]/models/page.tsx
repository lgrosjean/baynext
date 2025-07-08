import Link from "next/link";

import { Button } from "@workspace/ui/components/button";

export default async function ModelPage({ params }: { params: Promise<{ projectId: string }> }) {

    const { projectId } = await params;

    //   const models = await getModels(projectId);

    return (
        <section>
            <div className="flex items-start justify-between mb-4">
                <h1 className="text-2xl">My models</h1>
                <Button asChild>
                    <Link href={`/app/projects/${projectId}/models/new`}>
                        Create a model
                    </Link>
                </Button>
            </div>

        </section>
    );
}