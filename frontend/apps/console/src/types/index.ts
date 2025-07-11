export * from "./jobs";
export * from "./pipelines";
export * from "./enums"

import { Job } from "./jobs";
import { Pipeline } from "./pipelines";

export type JobWithPipeline = {
    job: Job
    pipeline: Pipeline
}