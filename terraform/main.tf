locals {
  apis = [
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com"
  ]
  repository_id = "baynext-docker-repo"
}

# Activate APIs for the project
resource "google_project_service" "services" {
  for_each = toset(local.apis)
  project  = var.project_id
  service  = each.value
}

# Create a Docker repository in Artifact Registry
# This repository will be used to store Docker images
resource "google_artifact_registry_repository" "docker_repo" {
  depends_on    = [google_project_service.services]
  project       = var.project_id
  location      = "europe-west1"
  repository_id = local.repository_id
  format        = "DOCKER"
}
