import { getUserProjects } from '@/actions/projects';

import { NewProjectDialog } from '@/components/projects/new-project-dialog';
import { ProjectsTable } from '@/components/projects/projects-table';
// import { apiClient } from '@/lib/api';

export default async function Overview() {

    const projects = await getUserProjects();

    // const me: {
    //     id: string;
    //     name: string;
    //     email: string;
    // } = await apiClient.get('/v1/me');

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