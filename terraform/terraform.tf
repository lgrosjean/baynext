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

    neon = {
      source = "kislerdm/neon"
    }
  }
}

provider "google" {
  project = var.project_id
}

# NEON_API_KEY is set in the environment
provider "neon" {}
