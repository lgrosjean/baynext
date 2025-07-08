export type Pipeline = {
    id: string
    projectId: string
    datasetId: string
    createdAt: Date
    updatedAt: Date
}

export type PipelineWithDatasetName = {
    pipeline: Pipeline
    dataset: {
        name: string
    }
}