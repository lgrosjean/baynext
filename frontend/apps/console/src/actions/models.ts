"use server"

import { db } from "@workspace/db/client";
import { models, jobs, pipelines } from "@workspace/db/schema";
import { eq, count, and } from "drizzle-orm";


export async function countNumberOfModels(projectId: string) {
    const result = await db
        .select({ count: count() })
        .from(models)
        .innerJoin(jobs, eq(models.jobId, jobs.id)) // ✅ join jobs first
        .innerJoin(pipelines, eq(jobs.pipelineId, pipelines.id)) // ✅ then join pipelines via jobs
        .where(eq(pipelines.projectId, projectId))
        .limit(1)
        .execute();

    if (!result || !result[0]) {
        throw new Error("Count not found");
    }
    return result[0].count;
}

export async function countNumberOfModelsDeployed(projectId: string) {
    const result = await db
        .select({ count: count() })
        .from(models)
        .innerJoin(jobs, eq(models.jobId, jobs.id)) // ✅ join jobs first
        .innerJoin(pipelines, eq(jobs.pipelineId, pipelines.id)) // ✅ then join pipelines via jobs
        .where(
            and(
                eq(pipelines.projectId, projectId), 
                eq(models.deployed, true)),
        )
        .limit(1)
        .execute();

    if (!result || !result[0]) {
        throw new Error("Count not found");
    }
    return result[0].count;
}