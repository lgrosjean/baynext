import { z } from "zod"

export const updateProjectNameSchema = z.object({
    name: z.string().min(2, {
        message: "Name must be at least 2 characters long",
    }),
})

export type updateProjectNameSchemaType = z.infer<typeof updateProjectNameSchema>