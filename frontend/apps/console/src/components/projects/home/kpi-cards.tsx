import { countNumberOfDatasets } from '@/actions/datasets';
import { countNumberOfModelsDeployed } from '@/actions/models';
import { countJobs } from '@/actions/jobs';

import {
    Card,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@workspace/ui/components/card"

import { Progress } from "@workspace/ui/components/progress"

const KpiCard = ({
    title,
    value,
    max,
}: {
    title: string,
    value: number,
    max: number,
}) => {
    return (
        <Card className="gap-2 rounded-sm shadow-none">
            <CardHeader>
                <CardDescription>{title}</CardDescription>
                <CardTitle className="text-2xl tabular-nums">{value}</CardTitle>
            </CardHeader>

            <CardFooter className="flex flex-col items-end">
                <Progress value={value/max*100}/>
                    <div className="text-sm text-muted-foreground">
                        {value} of {max}
                    </div>
            </CardFooter>
        </Card>
    );
}

export async function KpiCards({
    projectId
}: {
    projectId: string
}) {

    return (
        <div className="grid grid-cols-1 gap-4 md:grid-cols-3 my-4">

            <KpiCard
                title="Datasets"
                value={await countNumberOfDatasets(projectId)}
                max={5}
            />
            <KpiCard
                title="Jobs"
                value={await countJobs(projectId)}
                max={2}
            />
            <KpiCard
                title="Models"
                value={ await countNumberOfModelsDeployed(projectId)}
                max={2}
            />

        </div>
    );
}