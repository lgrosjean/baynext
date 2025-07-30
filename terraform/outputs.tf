output "neon_database_url" {
  value     = replace(neon_project.baynext_project.connection_uri, "postgres://", "postgresql://")
  sensitive = true
}
