import { pgTable, text, timestamp, json } from "drizzle-orm/pg-core";
import { relations } from "drizzle-orm";

import { projects } from "./projects";
import { kpiType, datasetFormat  } from "./enums";

export const datasets = pgTable("datasets", {
  id: text("id").primaryKey().$defaultFn(() => crypto.randomUUID()),
  projectId: text("project_id").notNull().references(() => projects.id, { onDelete: "cascade" }),
  name: text("name").notNull(),
  fileUrl: text("file_url").notNull(),
  format: datasetFormat("format").notNull().default("CSV"),
  uploadedAt: timestamp("uploaded_at").defaultNow().notNull(),
  geo: text("geo"),
  time: text("time").notNull(),
  kpi: text("kpi").notNull(),
  kpiType: kpiType("kpi_type"),
  population: text("population"),
  revenuePerKpi: text("revenue_per_kpi"),
  controls: text("controls").array(),
  medias: text("medias").array(),
  mediaSpend: text("media_spend").array(),
  mediaToChannel: json("media_to_channel"),
  mediaSpendToChannel: json("media_spend_to_channel"),
});

export const datasetRelations = relations(datasets, ({ one }) => ({
  project: one(projects, { fields: [datasets.projectId], references: [projects.id] }),
}));
