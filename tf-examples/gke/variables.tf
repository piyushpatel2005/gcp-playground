variable "project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "region" {
  type        = string
  description = "Default region for GCP resources"
}

variable "zone" {
  type        = string
  description = "Default zone for GCP resources"
}

variable "gke_num_nodes" {
  type        = number
  description = "Number of nodes for GKE cluster"
}

variable "machine_type" {
    type = string
    description = "GKE machine type"
}

variable "labels" {
  type = object({
    env = string
    team = string
  })
}