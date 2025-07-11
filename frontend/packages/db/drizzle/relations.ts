import { relations } from "drizzle-orm/relations";
import { projects, pipelines, datasets, models, jobs, user, account, modelVersions } from "./schema";

export const pipelinesRelations = relations(pipelines, ({one, many}) => ({
	project: one(projects, {
		fields: [pipelines.projectId],
		references: [projects.id]
	}),
	dataset: one(datasets, {
		fields: [pipelines.datasetId],
		references: [datasets.id]
	}),
	jobs: many(jobs),
}));

export const projectsRelations = relations(projects, ({one, many}) => ({
	pipelines: many(pipelines),
	models: many(models),
	user: one(user, {
		fields: [projects.userId],
		references: [user.id]
	}),
	datasets: many(datasets),
}));

export const datasetsRelations = relations(datasets, ({one, many}) => ({
	pipelines: many(pipelines),
	project: one(projects, {
		fields: [datasets.projectId],
		references: [projects.id]
	}),
}));

export const modelsRelations = relations(models, ({one, many}) => ({
	project: one(projects, {
		fields: [models.projectId],
		references: [projects.id]
	}),
	modelVersions: many(modelVersions),
}));

export const jobsRelations = relations(jobs, ({one, many}) => ({
	pipeline: one(pipelines, {
		fields: [jobs.pipelineId],
		references: [pipelines.id]
	}),
	modelVersions: many(modelVersions),
}));

export const accountRelations = relations(account, ({one}) => ({
	user: one(user, {
		fields: [account.userId],
		references: [user.id]
	}),
}));

export const userRelations = relations(user, ({many}) => ({
	accounts: many(account),
	projects: many(projects),
}));

export const modelVersionsRelations = relations(modelVersions, ({one}) => ({
	job: one(jobs, {
		fields: [modelVersions.jobId],
		references: [jobs.id]
	}),
	model: one(models, {
		fields: [modelVersions.modelId],
		references: [models.id]
	}),
}));