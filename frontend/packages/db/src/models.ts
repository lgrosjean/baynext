import { pgTable, text, timestamp, boolean} from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

import { projects } from "./projects";
import { jobs } from "./jobs";

export const models = pgTable("models", {
  id: text("id").primaryKey().$defaultFn(() => crypto.randomUUID()),
  // projectId: text("project_id").notNull().references(() => projects.id),
  jobId: text("job_id").notNull().references(() => jobs.id),
  // name: text("name").notNull(),
  // description: text("description"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  uri: text("uri").notNull(),
  deployed: boolean("deployed").notNull().default(false),
  // updatedAt: timestamp("updated_at").defaultNow(),
});

export const modelsRelations = relations(models, ({ one, many }) => ({
  // project: one(projects, { fields: [models.projectId], references: [projects.id] }),
  job: one(jobs, { fields: [models.jobId], references: [jobs.id] }),
  // versions: many(modelVersions),
}));

// export const modelVersions = pgTable("model_versions", {
//   id: text("id").primaryKey().$defaultFn(() => crypto.randomUUID()),
//   modelId: text("model_id").notNull().references(() => models.id),
//   jobId: text("job_id").notNull().references(() => jobs.id),
//   uri: text("uri").notNull(),
//   deployed: boolean("deployed").notNull().default(false),
//   createdAt: timestamp("created_at").defaultNow().notNull(),
// });

// export const modelVersionsRelations = relations(modelVersions, ({ one }) => ({
//   model: one(models, { fields: [modelVersions.modelId], references: [models.id] }),
//   job: one(jobs, { fields: [modelVersions.jobId], references: [jobs.id] }),
// }));
