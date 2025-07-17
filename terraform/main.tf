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

############################
# The following resources are for the Cloud Run ML job
############################

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
  role    = "roles/run.jobsExecutorWithOverrides"
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

##########################
# The following resources are for the Cloud Run backend service
##########################

# Create a service account for the Cloud Run backend service
resource "google_service_account" "cloud_run_backend_sa" {
  account_id   = "baynext-backend-sa"
  display_name = "Service Account for Baynext Backend"
  project      = var.project_id
}

# Grant the service account permissions to access Artifact Registry and invoke Cloud Run services
resource "google_project_iam_member" "cloud_run_backend_sa_artifact_registry_reader" {
  project = var.project_id
  role    = "roles/artifactregistry.reader"
  member  = google_service_account.cloud_run_backend_sa.member
}

resource "google_project_iam_member" "cloud_run_backend_sa_run_invoker" {
  project = var.project_id
  role    = "roles/run.servicesInvoker"
  member  = google_service_account.cloud_run_backend_sa.member
}

data "google_artifact_registry_docker_image" "backend_image" {
  location      = google_artifact_registry_repository.docker_repo.location
  repository_id = google_artifact_registry_repository.docker_repo.repository_id
  image_name    = "baynext-backend:latest"
}

# Create a Cloud Run service for the backend
resource "google_cloud_run_v2_service" "baynext_backend_service" {
  name     = "baynext-backend-service"
  location = local.location
  project  = var.project_id

  template {
    service_account = google_service_account.cloud_run_backend_sa.email
    containers {
      image = data.google_artifact_registry_docker_image.backend_image.self_link
      ports {
        container_port = 80
      }
    }
  }

}
