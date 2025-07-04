variable "backend_bucket" {
  description = "GCS bucket for Terraform state"
  type        = string
}

variable "project_id" {
  description = "GCP Project ID"
  type        = string
}
