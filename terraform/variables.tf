variable "project_id" {
  description = "GCP Project ID"
  type        = string
}

variable "auth_secret" {
  description = "Secret for authentication"
  type        = string
  sensitive   = false
}

variable "blob_read_write_token" {
  description = "Token for reading and writing blobs"
  type        = string
  sensitive   = true
}
