

import { KpiCards } from '@/components/projects/home/kpi-cards';

export default async function ProjectPage({ params }: { params: Promise<{ projectId: string }> }) {

  const { projectId } = await params;
  

  return (
    <section>
      <div className="mb-8">
        <h1 className="text-2xl">Project Overview</h1>
      </div>

      <KpiCards projectId={projectId}/>

      <div className="flex space-x-4">
        <button
          className="text-xs px-2 bg-blue-500 text-white rounded hover:bg-blue-600"
          // onClick={() => console.log('Create a new dataset')}
        >
          Create New Dataset
        </button>
        <button
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
          // onClick={() => console.log('Create a new pipeline')}
        >
          Create New Pipeline
        </button>
        <button
          className="px-4 py-2 bg-purple-500 text-white rounded hover:bg-purple-600"
          // onClick={() => console.log('Deploy a new model')}
        >
          Deploy New Model
        </button>
      </div>
    </section>
  )

}
