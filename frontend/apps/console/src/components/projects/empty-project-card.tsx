import Link from "next/link";
import { Button } from "@workspace/ui/components/button";
import { UploadCloud } from 'lucide-react';

export function EmptyProjectCard({ projectId }: { projectId: string }) {
  return (
    <div className="flex flex-col items-center justify-center text-center gap-4 my-24">
      <div className="rounded-full bg-muted p-4">
        <UploadCloud className="h-10 w-10 text-muted-foreground" />
      </div>
      <h2 className="text-xl font-semibold">No dataset created yet</h2>
      <p className="text-muted-foreground">Start by uploading a dataset to run your model.</p>
      <Button variant="default" asChild>
        <Link href={`/app/projects/${projectId}/datasets/new`}>
          Create a dataset
          </Link>
      </Button>
    </div>
  );
}