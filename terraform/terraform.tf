terraform {

  backend "gcs" {
    bucket = "tf-state-lgrosjean"
    prefix = "terraform/baynext/state"
  }

  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 6.0"
    }
  }
}

provider "google" {
  project = var.project_id
}