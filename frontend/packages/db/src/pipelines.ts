import { pgTable, text, timestamp, jsonb } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";
import { projects } from "./projects";
import { datasets } from "./datasets";
import { jobs } from "./jobs";

export const pipelines = pgTable("pipelines", {
  id: text("id").primaryKey().$defaultFn(() => crypto.randomUUID()),
  projectId: text("project_id").notNull().references(() => projects.id),
  datasetId: text("dataset_id").notNull().references(() => datasets.id),
  modelSpec: jsonb("model_spec").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});

export const pipelinesRelations = relations(pipelines, ({ one, many }) => ({
  project: one(projects, { fields: [pipelines.projectId], references: [projects.id] }),
  dataset: one(datasets, { fields: [pipelines.datasetId], references: [datasets.id] }),
  jobs: many(jobs),
}));
