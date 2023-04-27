provider "google" {
  credentials = file("credentials.json")
#   project = "[PROJECT_ID]"
#   region = "us-east1"
#   zone = "us-east1-d"
}

# resource "google_service_account" "dataproc_service" {
#   account_id   = "dataproc-service-agent1"
#   display_name = "Dataproc service agent"
# }
resource "google_storage_bucket" "warehouse" {
    project = "${var.project}"
    name          = "${var.project}"
    location      = "US"
    storage_class = "STANDARD"
    force_destroy = true

    uniform_bucket_level_access = true

# Prevent bucket from deletion
  # lifecycle {
  #   prevent_destroy = false
  # }
}

resource "google_dataproc_cluster" "mycluster" {
  name     = var.cluster_name
  region   = var.region
  graceful_decommission_timeout = "120s"
  labels = {
    cluster_type = "poc"
  }

  cluster_config {
    endpoint_config {
      enable_http_port_access = "true"
    }

    master_config {
      num_instances = 1
      machine_type  = "n2-standard-4"
    #   disk_config {
    #     boot_disk_type    = "pd-ssd"
    #     boot_disk_size_gb = 30
    #   }
    }

    worker_config {
      num_instances    = 0
      machine_type     = "e2-medium"
      disk_config {
        boot_disk_size_gb = 30
        num_local_ssds    = 1
      }
    }

    preemptible_worker_config {
      num_instances = 0
    }

    # Override or set some custom properties
    software_config {
      image_version = "2.0-debian10"
      override_properties = {
        "dataproc:dataproc.allow.zero.workers" = "true"
        "hive:hive.metastore.warehouse.dir" = "gs://${google_storage_bucket.warehouse.name}/hive/warehouse"
      }
    }

    gce_cluster_config {
      tags = ["foo", "bar"]
      # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
      # service_account = google_service_account.dataproc_service.email
      service_account_scopes = [
        "cloud-platform"
      ]
    }

    # You can define multiple initialization_action blocks
    # initialization_action {
    #   script      = "gs://dataproc-initialization-actions/stackdriver/stackdriver.sh"
    #   timeout_sec = 500
    # }
  }
}