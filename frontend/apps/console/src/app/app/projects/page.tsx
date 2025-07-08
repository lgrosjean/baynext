import { getUserProjects } from '@/actions/projects';

import { NewProjectDialog } from '@/components/projects/new-project-dialog';
import { ProjectsTable } from '@/components/projects/projects-table';

export default async function Overview() {


    const projects = await getUserProjects();

    return (
        <section>
            <div className="flex items-start justify-between">
                <h1 className="text-2xl">My projects</h1>
                <NewProjectDialog />
            </div>
            <div className="mt-4">
                <ProjectsTable projects={projects} />
            </div>
        </section>
    );
}