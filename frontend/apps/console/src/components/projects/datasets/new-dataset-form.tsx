"use client";

// Use a stepper: https://v0.dev/chat/shadcn-ui-stepper-XZVvYHpAWRh

import { useState } from "react"

import { upload } from '@vercel/blob/client';
import { createDataset } from "@/actions/datasets";
import { Select, SelectTrigger, SelectValue, SelectContent, SelectItem } from "@workspace/ui/components/select"
import { Button } from "@workspace/ui/components/button";
import { Separator } from "@workspace/ui/components/separator"
import {
  DropdownMenu,
  DropdownMenuCheckboxItem,
  DropdownMenuContent,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@workspace/ui/components/dropdown-menu"
import { DropdownMenuCheckboxItemProps } from "@radix-ui/react-dropdown-menu"
import Papa from 'papaparse';
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

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@workspace/ui/components/table"

import { toast } from "sonner"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"

import { Trash } from "lucide-react";

import { newDatasetSchema, NewDataset } from "@/validations/datasets";


export function NewDatasetForm({ projectId }: { projectId: string }) {

  const [columns, setColumns] = useState<string[]>([]);

  // 1. Define form.
  const form = useForm<NewDataset>({
    resolver: zodResolver(newDatasetSchema),
    defaultValues: {
      name: "",
      time: "",
      controls: [],
      medias: [],
      mediaSpend: [],
      mediaToChannel: {},
      mediaSpendToChannel: {},
    },
  })

  // 2. Define a submit handler.
  async function onSubmit(values: NewDataset) {
    // Do something with the form values.
    // ✅ This will be type-safe and validated.
    try {
      console.log(values)
      const newBlob = await upload(values.name, values.file, {
        access: 'public',
        handleUploadUrl: `/api/projects/${projectId}/dataset`,
      });
      const { file, ...datasetWithoutFile } = values;
      await createDataset(projectId, newBlob.url, datasetWithoutFile)
      toast.success(`Dataset ${values.name} created!`)

    } catch (error) {
      console.error(error)
      toast.error("Error creating dataset")
    }
  }

  return (

    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4 max-w-3xl">

        <div className="grid grid-cols-4 gap-8">
          <h3 className="text-lg col-span-1">General</h3>
          <div className="col-span-3 space-y-4">

            <DatasetNameField form={form} />
            <FileField form={form} setColumns={setColumns} />
            <KpiTypeField form={form} columns={columns} />
          </div>
        </div>



        <Separator className="my-4" />
        <div className="grid grid-cols-4 gap-8 overflow-clip">
          <div className="col-span-1">
            <h3 className="text-lg mb-4">Coords to columns</h3>
            <p className="text-xs text-muted-foreground text-justify">
              Map the column names to their corresponding variable types. <br /> <br />
              The required variable types are <code className="font-bold">time</code>, <code className="font-bold">kpi</code>, <code className="font-bold">population</code>, <code className="font-bold">controls</code>, <code className="font-bold">medias</code>, <code className="font-bold">spend</code>.
            </p>
          </div>

          <div className="col-span-3 space-y-4">

            {/* TODO: replace with command and popover */}
            <TimeColField form={form} columns={columns} />
            <ControlsColsField form={form} columns={columns} />
            <KpiColField form={form} columns={columns} />
            <GeoColField form={form} columns={columns} />
            <PopulationColField form={form} columns={columns} />
            <RevenuePerKpiColField form={form} columns={columns} />
            <MediaColsField form={form} columns={columns} />
            <MediaSpendColsField form={form} columns={columns} />
          </div>
        </div>

        <Separator className="my-4" />
        <MappingColsField form={form} columns={columns} />

        <Separator className="my-4" />
        <Button type="submit" disabled={!form.formState.isValid} >
          Create
        </Button>

      </form>
    </Form>
  )
}

function DatasetNameField({ form }: { form: any }) {
  return (<FormField
    control={form.control}
    name="name"
    render={({ field }) => (
      <FormItem>
        <FormLabel>Dataset Name</FormLabel>
        <FormControl>
          <Input placeholder="shadcn" {...field} />
        </FormControl>
        <FormDescription>
          The name of your dataset. This will be used to identify your dataset in the project.
        </FormDescription>
        <FormMessage />
      </FormItem>
    )}
  />
  )
}

function FileField({ form, setColumns }: { form: any, setColumns: (columns: string[]) => void }) {
  // {/* See: https://github.com/shadcn-ui/ui/discussions/2137 */}
  return (

    <FormField
      control={form.control}
      name="file"
      render={({ field: { value, onChange, ...fieldProps } }) => (
        <FormItem>
          <FormLabel>File</FormLabel>
          <FormControl>
            <Input {...fieldProps} type="file" placeholder="A short description of your project" accept="text/csv"
              onChange={(event) => {
                onChange(event.target.files && event.target.files[0])
                event.target.files && Papa.parse(event.target.files[0], {
                  header: true,
                  complete: function (results) {
                    if (results.meta.fields) {
                      results.meta.fields = results.meta.fields?.map(field => field === "" ? "<empty>" : field);
                      setColumns(results.meta["fields"])
                    }
                  }
                });
              }}
            />
          </FormControl>
          <FormDescription>
            The file you want to upload. Only CSV files are accepted.
          </FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  )
}

function KpiTypeField({ form, columns }: { form: any, columns: string[] }) {
  return (
    <FormField
      control={form.control}
      name="kpiType"
      render={({ field }) => (
        <FormItem>
          <FormLabel>KPI Type</FormLabel>
          <FormControl>

            <Select onValueChange={field.onChange} defaultValue={field.value} disabled={columns.length === 0}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Select a KPI type" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="revenue">Revenue</SelectItem>
                <SelectItem value="non-revenue">Non-Revenue</SelectItem>
              </SelectContent>
            </Select>
          </FormControl>
          <FormDescription>
            The type of KPI you want to predict. This will determine the type of model that is created.
          </FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  )
}

function TimeColField({ form, columns }: { form: any, columns: string[] }) {
  const label = "Time*"
  const description = "The column that contains the time series data."
  return (
    <FormField
      control={form.control}
      name="time"
      render={({ field }) => (
        <FormItem>
          <FormLabel>{label}</FormLabel>
          <FormControl>

            <Select onValueChange={field.onChange} defaultValue={field.value} disabled={columns.length === 0}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select a column" />
              </SelectTrigger>
              <SelectContent>
                {columns.length === 0 ? <SelectItem value="none" disabled>No columns found</SelectItem> :
                  columns.map((column) => (
                    <SelectItem key={column} value={column}>{column}</SelectItem>
                  ))}
              </SelectContent>
            </Select>
          </FormControl>
          <FormDescription>{description}</FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  )
}

function KpiColField({ form, columns }: { form: any, columns: string[] }) {
  const label = "KPI"
  const description = "Name of column containing `kpi` values in the input data."
  return (
    <FormField
      control={form.control}
      name="kpi"
      render={({ field }) => (
        <FormItem>
          <FormLabel>{label}</FormLabel>
          <FormControl>
            <Select onValueChange={field.onChange} defaultValue={field.value} disabled={columns.length === 0}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select a column" />
              </SelectTrigger>
              <SelectContent>
                {columns.length === 0 ? <SelectItem value="none" disabled>No columns found</SelectItem> :
                  columns.map((column) => (
                    <SelectItem key={column} value={column}>{column}</SelectItem>
                  ))}
              </SelectContent>
            </Select>
          </FormControl>
          <FormDescription>{description}</FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  )
}

function GeoColField({ form, columns }: { form: any, columns: string[] }) {
  const label = "Geo"
  const description = "Name of column containing geo values in the input data. This field is optional for a national model."

  return (
    <FormField
      control={form.control}
      name="geo"
      render={({ field }) => (
        <FormItem>
          <FormLabel>{label}</FormLabel>
          <FormControl>
            <Select onValueChange={field.onChange} defaultValue={field.value} disabled={columns.length === 0}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select a column" />
              </SelectTrigger>
              <SelectContent>
                {columns.length === 0 ? <SelectItem value="none" disabled>No columns found</SelectItem> :
                  columns.map((column) => (
                    <SelectItem key={column} value={column}>{column}</SelectItem>
                  ))}
              </SelectContent>
            </Select>
          </FormControl>
          <FormDescription>{description}</FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  )
}

function PopulationColField({ form, columns }: { form: any, columns: string[] }) {
  const label = "Population"
  const description = "Name of column containing population values in the input data. This field is optional for a national model."
  return (
    <FormField
      control={form.control}
      name="population"
      render={({ field }) => (
        <FormItem>
          <FormLabel>{label}</FormLabel>
          <FormControl>
            <Select onValueChange={field.onChange} defaultValue={field.value} disabled={columns.length === 0}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select a column" />
              </SelectTrigger>
              <SelectContent>
                {columns.length === 0 ? <SelectItem value="none" disabled>No columns found</SelectItem> :
                  columns.map((column) => (
                    <SelectItem key={column} value={column}>{column}</SelectItem>
                  ))}
              </SelectContent>
            </Select>
          </FormControl>
          <FormDescription>{description}</FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  )
}

function RevenuePerKpiColField({ form, columns }: { form: any, columns: string[] }) {
  const label = "Revenue per KPI"
  const description = "Name of column containing revenue_per_kpi values in the input data."
  return (
    <FormField
      control={form.control}
      name="revenuePerKpi"
      render={({ field }) => (
        <FormItem>
          <FormLabel>{label}</FormLabel>
          <FormControl>
            <Select onValueChange={field.onChange} defaultValue={field.value} disabled={columns.length === 0}>
              <SelectTrigger className="w-full">
                <SelectValue placeholder="Select a column" />
              </SelectTrigger>
              <SelectContent>
                {columns.length === 0 ? <SelectItem value="none" disabled>No columns found</SelectItem> :
                  columns.map((column) => (
                    <SelectItem key={column} value={column}>{column}</SelectItem>
                  ))}
              </SelectContent>
            </Select>
          </FormControl>
          <FormDescription>{description}</FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  )
}

function MediaColsField({ form, columns }: { form: any, columns: string[] }) {

  const label = "Medias"
  const description = "ist of column names containing media values in the input data."

  type Checked = DropdownMenuCheckboxItemProps["checked"]

  const [columnsSelected, setColumnsSelected] = useState<string[]>([])

  return (
    <FormField
      control={form.control}
      name="medias"
      render={({ field }) => (
        <FormItem>
          <FormLabel>{label}</FormLabel>
          <FormControl>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" disabled={columns.length === 0} className="justify-start text-ellipsis truncate font-normal">
                  {columnsSelected.length === 0 ? "Select columns" : columnsSelected.join(", ")}
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-full">
                <DropdownMenuSeparator />
                {columns.map((column) => (
                  <DropdownMenuCheckboxItem
                    key={column}
                    checked={field.value.includes(column) as Checked}
                    onCheckedChange={(checked) => {
                      if (checked) {
                        field.onChange([...field.value, column])
                        setColumnsSelected([...columnsSelected, column])
                      } else {
                        field.onChange(field.value.filter((value: string) => value !== column))
                        setColumnsSelected(columnsSelected.filter((value: string) => value !== column))
                      }
                    }}
                  >
                    {column}
                  </DropdownMenuCheckboxItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>

          </FormControl>
          <FormDescription>{description}</FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  )
}

function MediaSpendColsField({ form, columns }: { form: any, columns: string[] }) {

  const label = "Media Spend"
  const description = "List of column names containing media spend values in the input data."

  type Checked = DropdownMenuCheckboxItemProps["checked"]

  const [columnsSelected, setColumnsSelected] = useState<string[]>([])

  return (
    <FormField
      control={form.control}
      name="mediaSpend"
      render={({ field }) => (
        <FormItem>
          <FormLabel>{label}</FormLabel>
          <FormControl>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" disabled={columns.length === 0} className="justify-start text-ellipsis truncate font-normal">
                  {columnsSelected.length === 0 ? "Select columns" : columnsSelected.join(", ")}
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-full">
                <DropdownMenuSeparator />
                {columns.map((column) => (
                  <DropdownMenuCheckboxItem
                    key={column}
                    checked={field.value.includes(column) as Checked}
                    onCheckedChange={(checked) => {
                      if (checked) {
                        field.onChange([...field.value, column])
                        setColumnsSelected([...columnsSelected, column])
                      } else {
                        field.onChange(field.value.filter((value: string) => value !== column))
                        setColumnsSelected(columnsSelected.filter((value: string) => value !== column))
                      }
                    }}
                  >
                    {column}
                  </DropdownMenuCheckboxItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>

          </FormControl>
          <FormDescription>{description}</FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  )
}

function ControlsColsField({ form, columns }: { form: any, columns: string[] }) {

  const label = "Controls"
  const description = "List of column names containing controls values in the input data."

  type Checked = DropdownMenuCheckboxItemProps["checked"]

  const [columnsSelected, setColumnsSelected] = useState<string[]>([])

  return (
    <FormField
      control={form.control}
      name="controls"
      render={({ field }) => (
        <FormItem>
          <FormLabel>{label}</FormLabel>
          <FormControl>
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="outline" disabled={columns.length === 0} className="justify-start text-ellipsis truncate font-normal">
                  {columnsSelected.length === 0 ? "Select columns" : columnsSelected.join(", ")}
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-full">
                <DropdownMenuSeparator />
                {columns.map((column) => (
                  <DropdownMenuCheckboxItem
                    key={column}
                    checked={field.value.includes(column) as Checked}
                    onCheckedChange={(checked) => {
                      if (checked) {
                        field.onChange([...field.value, column])
                        setColumnsSelected([...columnsSelected, column])
                      } else {
                        field.onChange(field.value.filter((value: string) => value !== column))
                        setColumnsSelected(columnsSelected.filter((value: string) => value !== column))
                      }
                    }}
                  >
                    {column}
                  </DropdownMenuCheckboxItem>
                ))}
              </DropdownMenuContent>
            </DropdownMenu>

          </FormControl>
          <FormDescription>{description}</FormDescription>
          <FormMessage />
        </FormItem>
      )}
    />
  )
}

// media_spend: list[str],
// organic_media: list[str],
// non_media_treatments: list[str],

function MappingColsField({ form, columns }: { form: any, columns: string[] }) {

  type ColumnMapping = {
    channelName: string,
    mediaColumn: string,
    mediaSpendColumn: string,
  }

  const [columnMappings, setColumnMappings] = useState<ColumnMapping[]>([]);


  return (
    <div>
      <div className="flex items-start mb-5">
        <div>
          <h3 className="text-lg col-span-1">Column mapping</h3>
          <p className="text-xs text-muted-foreground text-justify">
            Map the media variables and the media spends to the designated channel names
          </p>
        </div>
        <Button type="button" variant="outline" className="ml-auto" onClick={() => {
          setColumnMappings([...columnMappings, { 
            channelName: `channel_${columnMappings.length}`,
            mediaColumn: "", 
            mediaSpendColumn: "" 
          }]);
        }
        }>
          New channel
        </Button>
      </div>
      
      <Table>
        <TableHeader>
          <TableRow className="hover:hover:bg-white">
            <TableHead>Column name</TableHead>
            
            <TableHead>
            <input {...form.register("mediaToChannel", { required: false })} type="hidden" />
              Media column
              </TableHead>
            <TableHead>
            <input {...form.register("mediaSpendToChannel", { required: false })} type="hidden"/>
              Media spend column
            </TableHead>
            <TableHead></TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {columnMappings.map((mapping, index) => (
            <TableRow key={index} className="hover:hover:bg-white">
              <TableCell>
                <Input placeholder="Channel name" 
                value={mapping.channelName} 
                onChange={(e) => {
                  const newMapping = [...columnMappings]
                  newMapping[index].channelName = e.target.value
                  setColumnMappings(newMapping)
                }} />
              </TableCell>
              <TableCell>
                <Select
                  onValueChange={(value) => {
                    const newMapping = [...columnMappings];
                    newMapping[index].mediaColumn = value;
                    setColumnMappings(newMapping);
                    form.setValue("mediaToChannel", {
                      ...form.getValues("mediaToChannel"),
                      [value]: columnMappings[index].channelName,
                    });
                  }}
                  value={mapping.mediaColumn}
                  disabled={columns.length === 0}
                >
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Select a column" />
                  </SelectTrigger>
                  <SelectContent>
                    {form.getValues("medias").map((column: string) => (
                      <SelectItem key={column} value={column}>
                      {column}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </TableCell>
              <TableCell>
                <Select
                  onValueChange={(value) => {
                    const newMapping = [...columnMappings];
                    newMapping[index].mediaSpendColumn = value;
                    setColumnMappings(newMapping);
                    form.setValue("mediaSpendToChannel", {
                      ...form.getValues("mediaSpendToChannel"),
                      [value]: columnMappings[index].channelName,
                    });
                  }}
                  value={mapping.mediaSpendColumn}
                  disabled={columns.length === 0}
                >
                  <SelectTrigger className="w-full">
                    <SelectValue placeholder="Select a column" />
                  </SelectTrigger>
                  <SelectContent>
                    {form.getValues("mediaSpend").map((column: string) => (
                      <SelectItem key={column} value={column}>
                      {column}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </TableCell>
              <TableCell>
                <Button
                  variant="ghost"
                  className=" text-gray-300 hover:text-red-500"
                  size="icon"
                  onClick={() => {
                    const newMapping = [...columnMappings];
                    newMapping.splice(index, 1);
                    setColumnMappings(newMapping);
                  }}
                >
                  <Trash className="size-4" />
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

    </div>
  )
}