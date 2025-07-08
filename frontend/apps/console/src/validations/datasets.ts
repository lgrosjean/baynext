import { z } from "zod"
import { KpiType } from "@/types/enums"

export const newDatasetSchema = z.object({
    name: z.string()
      .min(2, {
        message: "Dataset's name must be at least 2 characters.",
      })
      .max(50, {
        message: "Dataset's name must be at most 50 characters.",
      }),
    file: z.instanceof(File, 
      { message: "Please upload a valid CSV file." }
      ).refine((file) => file.type === "text/csv", {
      message: "Only CSV files are accepted.",
    }).refine((file) => file.size < 7000000, {
      message: 'Your resume must be less than 7MB.',
    }),
    time: z.string({message: "Please select a time column."}),
    kpi: z.string({message: "Please select a KPI column."}),
    kpiType: z.nativeEnum(KpiType, {
      errorMap: () => ({ message: "Please select a KPI type." }),
    }),
    geo: z.string().optional(),
    population: z.string().optional(),
    revenuePerKpi: z.string().optional(),
    controls: z.array(z.string()),
    medias: z.array(z.string()),
    mediaSpend: z.array(z.string()),
    mediaToChannel: z.record(z.string(), z.string()).optional(),
    mediaSpendToChannel: z.record(z.string(), z.string()).optional(), 
  })


export type NewDataset = z.infer<typeof newDatasetSchema>