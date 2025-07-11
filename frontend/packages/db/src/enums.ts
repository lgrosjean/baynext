import { pgEnum } from "drizzle-orm/pg-core";

export const kpiType = pgEnum("kpi_type", [
    "revenue",
    "non_revenue",
]);

export const datasetFormat = pgEnum("dataset_format", [
    "CSV",
]);

export const paidMediaPriorType = pgEnum("paid_media_prior_type", [
    "roi",
    "mroi",
    "coefficient",
]);

export const jobStatus = pgEnum("job_status", [
    "pending",
    "running",
    "completed",
    "failed",
]);