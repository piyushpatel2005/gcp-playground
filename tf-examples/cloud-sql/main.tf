locals {
  labels = var.labels
}

# CUSTOM NETWORK AND SUBNET
# =========================
# resource "google_compute_network" "vpc_network" {
#   name                    = "my-custom-mode-network"
#   auto_create_subnetworks = false
#   mtu                     = 1460
# }

# resource "google_compute_subnetwork" "default" {
#   name          = "my-custom-subnet"
#   ip_cidr_range = "10.0.1.0/24"
#   region        = var.region
#   network       = google_compute_network.vpc_network.id
# }

resource "random_id" "db_name_suffix" {
  byte_length = 8
}

resource "google_sql_database_instance" "master" {
  name = var.db_instance_name
  database_version = var.database_version
  region = "${var.region}"
  settings {
    tier = "db-${var.db_machine.type}"
  }

  deletion_protection = "false"
}

resource "google_sql_database" "database" {
  name = var.db_name
  instance = "${google_sql_database_instance.master.name}"
  charset = "utf8"
  collation = "utf8_general_ci"
}

resource "google_sql_user" "users" {
  name = "root"
  instance = "${google_sql_database_instance.master.name}"
  host = "%"
  password = "XXXXXXXXX"
}