resource "google_composer_environment" "composer_sbx" {
  name = "composer-test"
  project = "${var.project}"
  region = "${var.region}"
  config {
    node_config {
      network   = "${google_compute_network.network.name}"
      subnetwork = "${google_compute_subnetwork.subnet.name}"
    }

    software_config {
      image_version = "composer-2-airflow-2"

      env_variables = {
        "env" = "dev"
      }
    }

    workloads_config {
      scheduler {
        cpu = 1
        memory_gb = 3
      }

      web_server {
        cpu = 2
        memory_gb = 2
      }
      worker {
        cpu = 2
        memory_gb = 3
      }
    }
  }
  labels = var.labels
}

data "google_composer_environment" "composer_sbx" {
  name = google_composer_environment.composer_sbx.name

  depends_on = [
    google_composer_environment.composer_sbx
  ]
}

resource "google_storage_bucket_object" "dags" {
  name = "dags/${trimsuffix("${each.value}", ".py")}"
  for_each = fileset("./dags/", "*.py")
  source = "./dags/${each.value}"
  bucket = "${trimsuffix("${trimprefix("${local.dag_bucket}", "gs://")}", "/dags")}"
  depends_on = [
    google_composer_environment.composer_sbx
  ]
}
