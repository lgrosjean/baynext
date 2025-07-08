import { pgTable, varchar, timestamp, foreignKey, text, jsonb, integer, unique, json, boolean, pgEnum } from "drizzle-orm/pg-core"
import { sql } from "drizzle-orm"

export const jobStatus = pgEnum("job_status", ['pending', 'running', 'completed', 'failed'])
export const kpiType = pgEnum("kpi_type", ['revenue', 'non-revenue'])
export const paidMediaPriorType = pgEnum("paid_media_prior_type", ['roi', 'mroi', 'coefficient'])


export const subscribers = pgTable("subscribers", {
	email: varchar({ length: 255 }).primaryKey().notNull(),
	subscribedAt: timestamp("subscribed_at", { mode: 'string' }).defaultNow(),
});

export const pipelines = pgTable("pipelines", {
	id: text().primaryKey().notNull(),
	projectId: text("project_id").notNull(),
	datasetId: text("dataset_id").notNull(),
	modelSpec: jsonb("model_spec").notNull(),
	createdAt: timestamp("created_at", { mode: 'string' }).defaultNow().notNull(),
	updatedAt: timestamp("updated_at", { mode: 'string' }).defaultNow(),
}, (table) => [
	foreignKey({
			columns: [table.projectId],
			foreignColumns: [projects.id],
			name: "pipelines_project_id_projects_id_fk"
		}),
	foreignKey({
			columns: [table.datasetId],
			foreignColumns: [datasets.id],
			name: "pipelines_dataset_id_datasets_id_fk"
		}),
]);

export const models = pgTable("models", {
	id: text().primaryKey().notNull(),
	projectId: text("project_id").notNull(),
	createdAt: timestamp("created_at", { mode: 'string' }).defaultNow().notNull(),
	name: text().notNull(),
	description: text(),
	updatedAt: timestamp("updated_at", { mode: 'string' }).defaultNow(),
}, (table) => [
	foreignKey({
			columns: [table.projectId],
			foreignColumns: [projects.id],
			name: "models_project_id_projects_id_fk"
		}),
]);

export const jobs = pgTable("jobs", {
	id: text().primaryKey().notNull(),
	pipelineId: text("pipeline_id").notNull(),
	params: jsonb().notNull(),
	startedAt: timestamp("started_at", { mode: 'string' }),
	finishedAt: timestamp("finished_at", { mode: 'string' }),
	modelId: text("model_id"),
	status: jobStatus().default('pending').notNull(),
	retries: integer().default(0).notNull(),
}, (table) => [
	foreignKey({
			columns: [table.pipelineId],
			foreignColumns: [pipelines.id],
			name: "jobs_pipeline_id_pipelines_id_fk"
		}),
]);

export const user = pgTable("user", {
	id: text().primaryKey().notNull(),
	name: text(),
	email: varchar({ length: 255 }).notNull(),
	emailVerified: timestamp({ mode: 'string' }),
	password: varchar({ length: 255 }),
	createdAt: timestamp("created_at", { mode: 'string' }).defaultNow(),
	image: text(),
}, (table) => [
	unique("user_email_unique").on(table.email),
]);

export const account = pgTable("account", {
	userId: text().notNull(),
	type: text().notNull(),
	provider: text().notNull(),
	providerAccountId: text().notNull(),
	refreshToken: text("refresh_token"),
	accessToken: text("access_token"),
	expiresAt: integer("expires_at"),
	tokenType: text("token_type"),
	scope: text(),
	idToken: text("id_token"),
	sessionState: text("session_state"),
}, (table) => [
	foreignKey({
			columns: [table.userId],
			foreignColumns: [user.id],
			name: "account_userId_user_id_fk"
		}).onDelete("cascade"),
]);

export const projects = pgTable("projects", {
	id: text().primaryKey().notNull(),
	userId: text("user_id").notNull(),
	name: text().notNull(),
	description: text(),
	createdAt: timestamp("created_at", { mode: 'string' }).defaultNow().notNull(),
	updatedAt: timestamp("updated_at", { mode: 'string' }).defaultNow(),
}, (table) => [
	foreignKey({
			columns: [table.userId],
			foreignColumns: [user.id],
			name: "projects_user_id_user_id_fk"
		}).onDelete("cascade"),
]);

export const datasets = pgTable("datasets", {
	id: text().primaryKey().notNull(),
	projectId: text("project_id").notNull(),
	name: text().notNull(),
	fileUrl: text("file_url").notNull(),
	uploadedAt: timestamp("uploaded_at", { mode: 'string' }).defaultNow().notNull(),
	geo: text(),
	time: text().notNull(),
	kpi: text().notNull(),
	kpiType: kpiType("kpi_type"),
	population: text(),
	revenuePerKpi: text("revenue_per_kpi"),
	controls: text().array(),
	medias: text().array(),
	mediaSpend: text("media_spend").array(),
	mediaToChannel: json("media_to_channel"),
	mediaSpendToChannel: json("media_spend_to_channel"),
}, (table) => [
	foreignKey({
			columns: [table.projectId],
			foreignColumns: [projects.id],
			name: "datasets_project_id_projects_id_fk"
		}).onDelete("cascade"),
]);

export const modelVersions = pgTable("model_versions", {
	id: text().primaryKey().notNull(),
	modelId: text("model_id").notNull(),
	jobId: text("job_id").notNull(),
	uri: text().notNull(),
	deployed: boolean().default(false).notNull(),
	createdAt: timestamp("created_at", { mode: 'string' }).defaultNow().notNull(),
}, (table) => [
	foreignKey({
			columns: [table.jobId],
			foreignColumns: [jobs.id],
			name: "model_versions_job_id_jobs_id_fk"
		}),
	foreignKey({
			columns: [table.modelId],
			foreignColumns: [models.id],
			name: "model_versions_model_id_models_id_fk"
		}),
]);
