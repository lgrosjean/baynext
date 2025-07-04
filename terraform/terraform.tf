terraform {

  backend "gcs" {
    bucket = var.backend_bucket
    prefix = "terraform/baynext/state"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
}