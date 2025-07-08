'use server';

import { db } from '@workspace/db/client';
import { redis } from '@/lib/redis';
import { auth } from '@/auth';
import { projects} from '@workspace/db/schema';
import { eq } from 'drizzle-orm';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation'

const STATUS_KEY = (projectId: string) => `project:${projectId}:status`;

// ----------------------
// Create a new project
// ----------------------
export async function createProject({
  name,
  description,
}: {
  name: string;
  description?: string;
}) {
  const session = await auth();
  if (!session?.user?.id) {
    throw new Error('Unauthorized');
  }

  const project = {
    userId: session.user.id,
    name,
    description,
  }

  const [projectCreated] = await db
    .insert(projects)
    .values(project)
    .returning();

  if (!projectCreated) {
    throw new Error('Failed to create project');
  }

  // Optional: revalidate overview path
  revalidatePath('/app/projects');

  // await redis.set(STATUS_KEY(projectCreated.id), projectStatus.EMPTY);

  redirect(`/app/projects/${projectCreated.id}`);
}

// ----------------------
// List all user's projects
// ----------------------
export async function getUserProjects() {
  const session = await auth();

  if (!session?.user?.id) {
    throw new Error('Unauthorized');
  }

  const results = await db
    .select()
    .from(projects)
    .where(eq(projects.userId, session.user.id));

  return results;
}

// ----------------------
// Get project status by ID
// ----------------------
// export async function getProjectStatus(projectId: string): Promise<projectStatus> {
//   const status = await redis.get(STATUS_KEY(projectId));
//   return status as projectStatus;
// }

// ----------------------
// Delete project by ID
// ----------------------
export async function deleteProjectById(projectId: string) {

  const session = await auth();
  if (!session?.user?.id) {
    throw new Error('Unauthorized');
  }

  const project = await db
    .select()
    .from(projects)
    .where(eq(projects.id, projectId))
    .limit(1)
    .execute();

  if (!project || !project[0]) {
    throw new Error('Project not found');
  }

  if (project[0].userId !== session.user.id) {
    throw new Error('Unauthorized');
  }

  await db.delete(projects).where(eq(projects.id, projectId));
  await redis.del(STATUS_KEY(projectId));

  revalidatePath('/app/projects');
  redirect('/app/projects');
}

export async function getProjectById(projectId: string) {
  const session = await auth();
  if (!session?.user?.id) {
    throw new Error('Unauthorized');
  }

  const project = await db
    .select()
    .from(projects)
    .where(eq(projects.id, projectId))
    .limit(1)
    .execute();

  if (!project || !project[0]) {
    throw new Error('Project not found');
  }

  if (project[0].userId !== session.user.id) {
    throw new Error('Unauthorized');
  }

  return project[0];
}

export async function updateProjectName(
  projectId: string,
  name: string
) {
  const session = await auth();
  if (!session?.user?.id) {
    throw new Error('Unauthorized');
  }

  const project = await db
    .select()
    .from(projects)
    .where(eq(projects.id, projectId))
    .limit(1)
    .execute();

  if (!project || !project[0]) {
    throw new Error('Project not found');
  }

  if (project[0].userId !== session.user.id) {
    throw new Error('Unauthorized');
  }

  await db
    .update(projects)
    .set({ name })
    .where(eq(projects.id, projectId));

  revalidatePath(`/app/projects/${projectId}`);
}
