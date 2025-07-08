import { z } from "zod"

export const newModelSchema = z.object({
    name: z.string().min(2, {
        message: "Name must be at least 2 characters long",
    }),
    datasetId: z.string().uuid(),
})

export type newModelSchemaType = z.infer<typeof newModelSchema>