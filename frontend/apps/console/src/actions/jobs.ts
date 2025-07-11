"use server";
import { auth } from '@/auth';
import { newModelSchemaType } from '@/validations/models';
import { db } from "@workspace/db/client";
import { jobs, pipelines } from "@workspace/db/schema";
import { eq, count, desc } from "drizzle-orm";

import { JobWithPipeline, Job, Pipeline } from "@/types";

export async function countJobs(projectId: string) {
    const result = await db
        .select({ count: count() })
        .from(jobs)
        .innerJoin(pipelines, eq(jobs.pipelineId, pipelines.id))
        .where(eq(pipelines.projectId, projectId))
        .limit(1)
        .execute();

    if (!result || !result[0]) {
        throw new Error("Count not found");
    }
    return result[0].count;
}

export async function createJob(formData: newModelSchemaType, projectId: string) {
    
    const session = await auth();
    if (!session?.user?.id) {
        throw new Error('Unauthorized');
    }

    const ML_API_URL = process.env.ML_API_URL ?? "http://localhost:8000/api"

    const response =  await fetch(`${ML_API_URL}/run`, {
        method: 'POST',
        credentials: 'include',
        headers: {
            // 'Content-Type': 'multipart/form-data',
            'Content-Type': 'application/json',
            'Authorization':  `Bearer ${process.env.ML_API_SECRET_API_KEY}`
        },
        body: JSON.stringify({
            projectId,
            ...formData
        })
    })

    if (!response.ok) {
        throw new Error(`Failed to create job, ${response.status} ${response.statusText}`);
    }

    return response.json()
}

export async function getJobs(projectId: string): Promise<JobWithPipeline[]> {
    const session = await auth();
    if (!session?.user?.id) {
        throw new Error('Unauthorized');
    }

    const result = await db
        .select({ job: jobs, pipeline: pipelines })
        .from(jobs)
        .innerJoin(pipelines, eq(jobs.pipelineId, pipelines.id))
        .where(eq(pipelines.projectId, projectId))
        .orderBy(desc(jobs.startedAt))
        .execute();

    if (!result) {
        throw new Error("Jobs not found");
    }
    return result as {job: Job, pipeline: Pipeline}[];
}