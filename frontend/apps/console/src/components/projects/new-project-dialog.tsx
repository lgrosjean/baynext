"use client";

import { useState } from "react"

import { createProject } from "@/actions/projects"

import { Button } from "@workspace/ui/components/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@workspace/ui/components/dialog"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@workspace/ui/components/form"
import { Input } from "@workspace/ui/components/input"
import { toast } from "sonner"

import { Plus } from 'lucide-react'

import { zodResolver } from "@hookform/resolvers/zod"
import { set, useForm } from "react-hook-form"
import { z } from "zod"

const newProjectSchema = z.object({
  name: z.string()
    .min(2, {
      message: "Project's name must be at least 2 characters.",
    })
    .max(50, {
      message: "Project's name must be at most 50 characters.",
    }),
  description: z.string().optional(),
})

export function NewProjectDialog() {

  const [open, setOpen] = useState(false);

  // 1. Define form.
  const form = useForm<z.infer<typeof newProjectSchema>>({
    resolver: zodResolver(newProjectSchema),
    defaultValues: {
      name: "",
    },
  })

  // 2. Define a submit handler.
  async function onSubmit(values: z.infer<typeof newProjectSchema>) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    try {
      await createProject(values)

      setOpen(false)
      toast.success(`Project ${values.name} created`)
      
    } catch (error) {
      console.error(error)
      setOpen(false)
      toast.error("Error creating project")
    }
  }

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogTrigger asChild>
        <Button variant="default">
          <Plus className="mr-2 h-4 w-4" />
          New project</Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
        <DialogHeader>
          <DialogTitle>Create project</DialogTitle>
          <DialogDescription>
            Create a new project to start tracking your work.
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">

            <FormField
              control={form.control}
              name="name"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Name</FormLabel>
                  <FormControl>
                    <Input placeholder="shadcn" {...field} />
                  </FormControl>
                  {/* <FormDescription>
                    Your project display name.
                  </FormDescription> */}
                  <FormMessage />
                </FormItem>
              )}
            />

            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Description</FormLabel>
                  <FormControl>
                    <Input placeholder="A short description of your project" {...field} />
                  </FormControl>
                  {/* <FormDescription>
                    A short description of your project.
                  </FormDescription> */}
                  <FormMessage />
                </FormItem>
              )}
            />


            <DialogFooter>
              <Button type="submit">Create</Button>
            </DialogFooter>

          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}
