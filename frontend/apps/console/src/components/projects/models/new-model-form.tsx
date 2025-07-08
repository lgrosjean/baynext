"use client";
import Link from "next/link";

import { useEffect, useState } from "react";

import { Button } from "@workspace/ui/components/button";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@workspace/ui/components/select"

import { getDatasets } from "@/actions/datasets";

import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@workspace/ui/components/form"
import { Separator } from "@workspace/ui/components/separator";
import { Input } from "@workspace/ui/components/input"
import { toast } from "sonner"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"

import { newModelSchema, newModelSchemaType } from "@/validations/models";


export function NewModelForm({
  projectId,
  datasetId,
}: {
  projectId: string,
  datasetId?: string,
}) {

  // 1. Define form.
  const form = useForm<newModelSchemaType>({
    resolver: zodResolver(newModelSchema),
    defaultValues: {
      name: "",
      datasetId: datasetId || "",
    },
  });

  const [datasets, setDatasets] = useState<{ id: string; name: string }[]>([]);

  useEffect(() => {
    async function fetchDatasets() {
      try {
        const fetchedDatasets = await getDatasets(projectId);
        setDatasets(fetchedDatasets);
      } catch (error) {
        console.error("Error fetching datasets:", error);
        toast.error("Failed to load datasets.");
      }
    }
    form.setFocus("name")
    fetchDatasets();
  }, [projectId, form.setFocus]);



  // 2. Define a submit handler.
  async function onSubmit(values: newModelSchemaType) {

    try {
      console.log(values)
      // const response = await createJob(values, projectId)
      // console.log(response)
      toast.success(`Job created!`)

    } catch (error) {
      console.error(error)
      toast.error("Error creating dataset: " + String(error))
    }
  }

  return (

    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 max-w-1/2">

        <ModelNameField form={form} />
        <DatasetNameField form={form} datasets={datasets} />

        <Separator className="my-4" />
        <h3 className="text-lg font-semibold">Model specifications</h3>


        <div className="flex items-center gap-2">
          <Button type="submit" disabled={!form.formState.isValid}>
            Create model
          </Button>
          <Button variant="outline" asChild>
            <Link href={`/app/projects/${projectId}/models`}>
              Cancel
            </Link>
          </Button>
        </div>

      </form>
    </Form>
  )
}

function ModelNameField({ form }: { form: any }) {
  return (
    <FormField
      control={form.control}
      name="name"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Name</FormLabel>
          <FormControl>
            <Input placeholder="My Model" {...field}/>
          </FormControl>
          {/* <FormDescription>
            The name of your model. This will be used to identify your model in the project.
          </FormDescription> */}
          <FormMessage />
        </FormItem>
      )}
    />
  )
}

function DatasetNameField({
  form,
  datasets,
}: {
  form: any,
  datasets: { id: string; name: string }[],
}) {

  return (
    <FormField
      control={form.control}
      name="datasetId"
      render={({ field }) => (
        <FormItem>
          <FormLabel>Dataset</FormLabel>
          <FormControl>
            <Select onValueChange={field.onChange} defaultValue={field.value} >
              <FormItem>
                <SelectTrigger className="w-full">
                  <SelectValue placeholder="Select a dataset"  />
                </SelectTrigger>
              </FormItem>
              <SelectContent>
                {datasets.map((dataset) => (
                  <SelectItem key={dataset.id} value={dataset.id}>
                    {dataset.name}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </FormControl>
          {/* <FormDescription>
            The name of your model. This will be used to identify your model in the project.
          </FormDescription> */}
          <FormMessage />
        </FormItem>
      )}
    />
  )
}

