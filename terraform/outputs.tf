output "cloud_run" {
  value       = google_cloud_run_v2_job.baynext_ml_job.uri
  description = "The URI of the Cloud Run job for Baynext ML"
}
