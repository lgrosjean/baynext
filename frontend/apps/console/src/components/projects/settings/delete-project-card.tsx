import { Card, CardHeader, CardTitle, CardDescription, CardFooter } from "@workspace/ui/components/card"
import { Button } from "@workspace/ui/components/button"

import { deleteProjectById } from "@/actions/projects"

export function DeleteProjectCard({ projectId }: { projectId: string }) {

  const handleDeleteProject = async () => {
    "use server"
    await deleteProjectById(projectId)
  }

  return (
    <Card className="border-destructive shadow-none">
      <CardHeader>
        <CardTitle>Delete Project</CardTitle>
        <CardDescription>
          This action cannot be undone. This will permanently delete this project and all its data.
        </CardDescription>
      </CardHeader>
      <CardFooter>
      <form action={handleDeleteProject}>
        <Button variant="destructive">
          Delete
        </Button>
      </form>
      </CardFooter>
    </Card>
  )
}
