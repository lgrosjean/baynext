import { getJobs } from "@/actions/jobs";
import { getPipelines } from "@/actions/pipelines";

import { JobsTable } from "@/components/projects/pipelines/jobs/jobs-table";
import { TemplatesTable } from "@/components/projects/pipelines/templates/templates-tables";


import {
    Tabs,
    TabsContent,
    TabsList,
    TabsTrigger,
} from "@workspace/ui/components/tabs"

export default async function ModelPage({ params }: { params: Promise<{ projectId: string }> }) {

    const { projectId } = await params;

    const jobs = await getJobs(projectId);
    const pipelines = await getPipelines(projectId);

    return (
        <section>
            <div className="flex items-start justify-between mb-4">
                <h1 className="text-2xl">Pipelines</h1>
                {/* <Button asChild>
                    <Link href={`/app/projects/${projectId}/models/new`}>
                        Create a model
                    </Link>
                </Button> */}
            </div>

            <Tabs defaultValue="templates" >
                <TabsList >
                    <TabsTrigger value="templates">Templates</TabsTrigger>
                    <TabsTrigger value="jobs">Jobs</TabsTrigger>
                </TabsList>
                <TabsContent value="jobs">
                <JobsTable jobs={jobs} />
                </TabsContent>
                <TabsContent value="templates">
                    <p className="text-sm text-muted-foreground mb-8">
                        Templates are reusable components that can be used to create pipelines.
                    </p>
                    <TemplatesTable pipelines={pipelines} />
                </TabsContent>
                
            </Tabs>

            

        </section>
    );
}