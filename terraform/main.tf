locals {
  repository_id = "baynext-docker-repo"
}
resource "google_artifact_registry_repository" "repo" {
  project = var.project_id
  location      = "europe-west1"
  repository_id = local.repository_id
  format        = "DOCKER"
}