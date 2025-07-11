import { UpdateProjectCard } from "@/components/projects/settings/update-project-name-card";
import { DeleteProjectCard } from "@/components/projects/settings/delete-project-card";

import { getProjectById } from "@/actions/projects";

export default async function SettingsPage({ params } : {params: Promise<{
    projectId: string
  }>}) {

    const { projectId } = await params
    // Fetch project details
    const project = await getProjectById(projectId);

    return (
        <section>
            
            <div className="flex items-start justify-between mb-4">
                <h1 className="text-2xl">Settings</h1>
            </div>

            <div className="space-y-5">
                <UpdateProjectCard project={project} />
                <DeleteProjectCard projectId={projectId} />
            </div>

        </section>
    );
}