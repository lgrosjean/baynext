

import { KpiCards } from '@/components/projects/home/kpi-cards';

export default async function ProjectPage({ params }: { params: Promise<{ projectId: string }> }) {

  const { projectId } = await params;
  

  return (
    <section>
      <div className="mb-8">
        <h1 className="text-2xl">Project Overview</h1>
      </div>

      <KpiCards projectId={projectId}/>

    </section>
  )

}
