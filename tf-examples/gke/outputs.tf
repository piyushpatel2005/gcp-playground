output "region" {
  value       = var.region
  description = "google cloud region"
}

output "project_id" {
  value       = var.project_id
  description = "Project ID for GCP Project"
}

output "kubernetes_cluster_name" {
  value = google_container_cluster.primary.name
}

output "kubernetes_cluster_host" {
  value = google_container_cluster.primary.endpoint
}