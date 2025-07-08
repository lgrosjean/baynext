"use client";

import { useRouter } from 'next/navigation'

import { Card, CardHeader, CardTitle, CardDescription, CardFooter } from "@workspace/ui/components/card"
import { Button } from "@workspace/ui/components/button"
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from "@workspace/ui/components/form"
import { Input } from "@workspace/ui/components/input"
import { toast } from "sonner"

import { updateProjectName } from "@/actions/projects"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"

import { updateProjectNameSchema, updateProjectNameSchemaType } from "@/validations/projects";

export function UpdateProjectCard({ project }: { project: {
    id: string, name: string }}) {

    const form = useForm<updateProjectNameSchemaType>({
        resolver: zodResolver(updateProjectNameSchema),
        defaultValues: {
            name: project.name,
        },
    });

    const router = useRouter()
    
    // 2. Define a submit handler.
    async function onSubmit(values: updateProjectNameSchemaType) {

        try {
            await updateProjectName(project.id, values.name)
            router.push(`/app/projects/${project.id}/settings`)
            toast.success(`Project's name updated!`)

        } catch (error) {
            console.error(error)
            toast.error("Error creating dataset: " + String(error))
        }
    }

    return (
        <Card className="shadow-none">

            <CardHeader>
                <CardTitle>Update project's name</CardTitle>
                <CardDescription>
                    This action will update the project's name.
                </CardDescription>
            </CardHeader>

            <CardFooter >

                <Form {...form}>
                    <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 w-1/2">

                        <FormField
                            name="name"
                            render={({ field }) => (
                                <FormItem>
                                    <FormLabel>Project name</FormLabel>
                                    <FormControl>
                                        <Input
                                            placeholder="Project name"
                                            value={field.value}
                                            // {...field}
                                            onChange={(e) => {
                                                field.onChange(e);
                                            }}
                                        />
                                    </FormControl>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />

                        <Button type="submit">
                            Update
                        </Button>

                    </form>
                </Form>
            </CardFooter>
        </Card>
    )
}
