'use server';

import { head } from '@vercel/blob';

import { revalidatePath } from 'next/cache';

import { db } from '@workspace/db/client';
import { KpiType } from "@/types/enums"
import { datasets } from '@workspace/db/schema';
import { NewDataset } from '@/validations/datasets';
import { eq, and, count } from 'drizzle-orm';
import { redirect } from 'next/navigation'

export async function refreshDatasetsPage(projectId: string) {
  revalidatePath(`/app/projects/${projectId}/datasets`);
}


export async function getDatasets(projectId: string) {
  return await db
    .select()
    .from(datasets)
    .where(eq(datasets.projectId, projectId));
}

export async function countNumberOfDatasets(projectId: string) {  
  const result = await db
    .select({ count: count() })
    .from(datasets)
    .where(eq(datasets.projectId, projectId))
    .limit(1)
    .execute();

  if (!result || !result[0]) {
    throw new Error('Count not found');
  }
  return result[0].count;
}

export async function getDataset(
  projectId: string,
  datasetId: string
) {
  const dataset = await db
    .select()
    .from(datasets)
    .where(and(
      eq(datasets.projectId, projectId),
      eq(datasets.id, datasetId)
    ))
    .limit(1)
    .execute();

  if (!dataset || !dataset[0]) {
    throw new Error('Dataset not found');
  }
  return dataset[0];
}

export async function getDatasetMetadata(
  projectId: string,
  datasetId: string
) {
  const dataset = await db
    .select()
    .from(datasets)
    .where(and(
      eq(datasets.projectId, projectId),
      eq(datasets.id, datasetId)
    ))
    .limit(1)
    .execute();

  if (!dataset || !dataset[0]) {
    throw new Error('Dataset not found');
  }
  
  const { fileUrl } = dataset[0];
  const metadata = await head(fileUrl);

  if (!metadata) {
    throw new Error('Metadata not found');
  }

  return metadata;
}

export async function createDataset(
  projectId: string, 
  fileUrl: string,
  newDataset: {
    name: string;
    time: string;
    kpi: string;
    kpiType: KpiType;
    geo?: string;
    population?: string;
    revenuePerKpi?: string;
    controls?: string[];
    medias?: string[];
    mediaSpend?: string[];
    mediaToChannel?: Record<string, string>;
    mediaSpendToChannel?: Record<string, string>;
  }) {

  console.log('Creating dataset', {
    projectId,
    fileUrl,
    newDataset,
  }
  )

  const dataset = {
    ...newDataset,
    fileUrl,
    projectId: projectId,
  };

  const [datasetCreated] = await db
    .insert(datasets)
    .values(dataset)
    .returning();

  if (!datasetCreated) {
    throw new Error('Failed to create dataset');
  }

  revalidatePath(`/app/projects/${projectId}`);
  redirect(`/app/projects/${projectId}/datasets`);

}

export async function deleteDataset(
  projectId: string,
  datasetId: string
) {
  await db
    .delete(datasets)
    .where(and(
      eq(datasets.projectId, projectId),
      eq(datasets.id, datasetId)
    ));

  revalidatePath(`/app/projects/${projectId}/datasets`);
  redirect(`/app/projects/${projectId}/datasets`);
}