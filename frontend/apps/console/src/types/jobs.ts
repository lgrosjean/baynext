import { JobStatus } from "./enums";


export type Job = {
    id: string;
    pipelineId: string;
    params: object;
    status: JobStatus;
    startedAt: Date | null;
    finishedAt: Date | null;
    error: string | null;
};
