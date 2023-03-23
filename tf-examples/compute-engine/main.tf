# Terraform Backend bucket
resource "random_id" "bucket_prefix" {
    byte_length = 8
}

resource "google_storage_bucket" "default" {
    project       = var.project
    name          = "${random_id.bucket_prefix.hex}-bucket-tfstate"
    # force_destroy = false
    location      = "US"
    storage_class = "STANDARD"
    # Enable versioning to restore if you ever have to.
    versioning {
        enabled = true
    }
    labels = "${merge(local.resource_tags, var.tags)}"
}

data "google_compute_instance" "webserver" {
    name = "webserver-data"
    zone = var.zone

    depends_on = [
      google_compute_instance.webserver
    ]
}

# Locals
locals {
    resource_tags = {
        team = "gcp-wls"
        environment = "playground"
    }
}

# CUSTOM NETWORK AND SUBNET
# =========================
resource "google_compute_network" "vpc_network" {
  name                    = "my-custom-mode-network"
  auto_create_subnetworks = false
  mtu                     = 1460
}

resource "google_compute_subnetwork" "default" {
  name          = "my-custom-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.vpc_network.id
}

# CREATE COMPUTE ENGINE FOR WEBSERVER
# ===================================
resource "google_compute_instance" "webserver" {
  name         = "flask-vm"
  machine_type = "e2-medium"
  zone         = var.zone
  tags         = ["ssh"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  # Install Flask
  metadata_startup_script = "sudo apt-get update; sudo apt-get install -yq build-essential python3-pip rsync; pip install flask"

  network_interface {
    subnetwork = google_compute_subnetwork.default.id

    access_config {
      # Include this section to give the VM an external IP address
    }
  }
}


# RESERVING EXTERNAL IP ADDRESS WITH VM
# =====================================
resource "google_compute_address" "external_with_subnet_and_address" {
  name         = "my-external-address"
  # subnetwork   = google_compute_subnetwork.default.id
  address_type = "EXTERNAL"
  # address      = "10.0.42.42" # address can be specified only for INTERNAL address_type
  region       = "us-west1"
}

# Create a single Compute Engine instance
resource "google_compute_instance" "dbserver" {
  name         = "database-vm"
  machine_type = "e2-small"
  zone         = var.zone
  tags         = ["ssh"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
    }
  }

  network_interface {
    subnetwork = google_compute_subnetwork.default.id

    access_config {
      # Include this section to give the VM an external IP address
      nat_ip = google_compute_address.external_with_subnet_and_address.address
    }
  }
}

# USING AVAILABLE SSH KEY FOR WEB-SERVER
# ======================================
