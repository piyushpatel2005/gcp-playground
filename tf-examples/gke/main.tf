resource "google_compute_network" "vpc" {
  name                    = "${var.project_id}-gke-vpc"
  auto_create_subnetworks = "false"
}

# Subnet
resource "google_compute_subnetwork" "subnet" {
  name          = "${var.project_id}-gke-subnet"
  region        = var.region
  network       = google_compute_network.vpc.name
  ip_cidr_range = "10.10.0.0/24"
}

resource "google_container_cluster" "primary" {
  name     = "${var.project_id}-gke"
  location = var.zone

  # Clusters need node pool defined, so we define single node pool
  initial_node_count = 1
  remove_default_node_pool = true
#   node_pool = google_container_node_pool.primary_nodes
#   node_pool_defaults = google_container_node_pool.primary_nodes
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "${google_container_cluster.primary.name}-pool"
  location   = var.zone # specify region if you want regional cluster, i.e. nodes = num_node * num_zones in that region
  cluster    = google_container_cluster.primary.name
  node_count = var.gke_num_nodes

  node_config {
    preemptible = false
    oauth_scopes = [
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring",
    ]

    labels = var.labels

    machine_type = var.machine_type
    tags         = ["gke-node", "${var.project_id}-gke"]
    metadata = {
      disable-legacy-endpoints = "true"
    }
  }
}