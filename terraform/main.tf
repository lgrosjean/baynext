locals {
  apis = [
    "run.googleapis.com",
    "artifactregistry.googleapis.com",
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com"
  ]
  repository_id = "baynext-docker-repo"
  location      = "europe-west1"
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
  location      = local.location
  repository_id = local.repository_id
  format        = "DOCKER"

  cleanup_policies {
    id     = "keep-last-2"
    action = "KEEP"

    most_recent_versions {
      keep_count = 2
    }
  }
}

# Create a service account for the Cloud Run job
resource "google_service_account" "cloud_run_job_sa" {
  account_id   = "baynext-ml-job-sa"
  display_name = "Service Account for Baynext ML Job"
  project      = var.project_id
}

# Grant the service account permissions to run jobs and access Artifact Registry
resource "google_project_iam_member" "cloud_run_job_sa_artifact_registry_reader" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = google_service_account.cloud_run_job_sa.member
}

resource "google_project_iam_member" "cloud_run_job_sa_run_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = google_service_account.cloud_run_job_sa.member
}

resource "google_cloud_run_v2_job" "baynext_ml_job" {
  name     = "baynext-ml-job"
  location = local.location
  project  = var.project_id

  template {
    template {
      service_account = google_service_account.cloud_run_job_sa.email
      containers {
        image = "${local.location}-docker.pkg.dev/${var.project_id}/${local.repository_id}/baynext-ml:latest"
      }
    }
  }
}
