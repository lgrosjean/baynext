output "neon_database_url" {
  description = "value of the Neon database URL"
  value       = replace(neon_project.baynext_project.connection_uri, "postgres://", "postgresql://")
  sensitive   = true
}
