output "cloud_run" {
  value       = google_cloud_run_v2_job.baynext_ml_job
  description = "The Cloud Run job for Baynext ML"
}
