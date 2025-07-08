import { pgTable, text, timestamp, jsonb, integer } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

import { pipelines } from "./pipelines";
import { jobStatus } from "./enums";

export const jobs = pgTable("jobs", {
  id: text("id").primaryKey().$defaultFn(() => crypto.randomUUID()),
  pipelineId: text("pipeline_id").notNull().references(() => pipelines.id),
  params: jsonb("params").notNull(),
  status: jobStatus("status").notNull().default("pending"),
  startedAt: timestamp("started_at"),
  finishedAt: timestamp("finished_at"),
  // retries: integer("retries").notNull().default(0),
  error: text("error"),
});

export const jobsRelations = relations(jobs, ({ one }) => ({
  pipeline: one(pipelines, { fields: [jobs.pipelineId], references: [pipelines.id] }),
}))
