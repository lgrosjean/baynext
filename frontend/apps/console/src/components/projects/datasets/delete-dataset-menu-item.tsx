"use client";

import { useState } from "react"

import { deleteDataset } from "@/actions/datasets";

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

import { Delete } from 'lucide-react'

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { z } from "zod"

import { DropdownMenuItem } from "@workspace/ui/components/dropdown-menu"

import { Dataset } from "@/types/datasets"



export function DeleteDatasetMenuItem({ dataset }: { dataset: Dataset}) {

    const [open, setOpen] = useState(false);

    const DeleteDatasetSchema = z.object({
        name: z.literal(dataset.fileName, {
                message: "Name must match the dataset's name",
            })
    })

    // 1. Define form.
    const form = useForm<z.infer<typeof DeleteDatasetSchema>>({
        resolver: zodResolver(DeleteDatasetSchema),
        defaultValues: {
            name: "",
        },
    })

    // 2. Define a submit handler.
    async function onSubmit(values: z.infer<typeof DeleteDatasetSchema>) {
        try {
            await deleteDataset(dataset.projectId, dataset.id)
            toast.success(`Dataset ${values.name} deleted`)
            setOpen(false)

        } catch (error) {
            console.error(error)
            setOpen(false)
            toast.error("Failed to delete dataset")
        }
    }

    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
                <DropdownMenuItem variant="destructive" onSelect={(e) => e.preventDefault()} className="cursor-pointer">
                    <Delete />
                    Delete
                </DropdownMenuItem>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Delete the dataset</DialogTitle>
                    <DialogDescription>
                        Confirm the deletion by giving the dataset's name.
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
                                        <Input placeholder={dataset.fileName} {...field} />
                                    </FormControl>
                                    <FormDescription>
                                        The dataset to delete's name.
                                    </FormDescription>
                                    <FormMessage />
                                </FormItem>
                            )}
                        />



                        <DialogFooter>
                            <Button type="submit" variant="destructive" 
                            disabled={!form.formState.isValid}
                            >Delete</Button>
                        </DialogFooter>

                    </form>
                </Form>
            </DialogContent>
        </Dialog>
    )
}
