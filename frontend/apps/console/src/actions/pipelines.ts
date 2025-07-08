"use server";

import { auth } from '@/auth';
import { db } from "@workspace/db/client";
import { pipelines, datasets, jobs } from "@workspace/db/schema";
import { eq, desc, sql } from "drizzle-orm";

export type PipelineWithDatasetNameAndJobs = {
    pipeline: {
        id: string;
        projectId: string;
        createdAt: Date;
        updatedAt: Date;
    };
    dataset: {
        id: string;
        name: string;
    };
    jobs: string[];
}

export async function getPipelines(projectId: string): Promise<PipelineWithDatasetNameAndJobs[]> {
    const session = await auth();
    if (!session?.user?.id) {
        throw new Error('Unauthorized');
    }

    const result = await db
        .select({
            pipeline: {
                id: pipelines.id,
                projectId: pipelines.projectId,
                createdAt: pipelines.createdAt,
                updatedAt: pipelines.updatedAt,
            }, 
            dataset: { 
                name: datasets.name,
                id: datasets.id,
            },
            jobs: sql<string[]>`array_agg(jobs.id ORDER BY jobs.started_at DESC)`.as('jobs')
        })
        .from(pipelines)
        .innerJoin(datasets, eq(pipelines.datasetId, datasets.id))
        .leftJoin(jobs, eq(pipelines.id, jobs.pipelineId))
        .where(eq(pipelines.projectId, projectId))
        .groupBy(
            pipelines.id, 
            datasets.name, 
            datasets.id,
            pipelines.createdAt, 
            pipelines.updatedAt,
            pipelines.projectId
        )
        .orderBy(desc(pipelines.createdAt))
        .execute();

    return result;
}