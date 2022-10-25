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
    }
  }
}

data "google_composer_environment" "composer_sbx" {
  name = google_composer_environment.composer_sbx.name

  depends_on = [
    google_composer_environment.composer_sbx
  ]
}

output "composer_debug" {
  value = data.google_composer_environment.composer_sbx.config.0.dag_gcs_prefix
}

output "composer_dag_bucket" {
  value = "${trimsuffix("${trimprefix("${local.dag_bucket}", "gs://")}", "/dags")}"
  description = "Bucket name for Composer"
}
locals {
  dag_bucket = data.google_composer_environment.composer_sbx.config.0.dag_gcs_prefix
}

resource "google_storage_bucket_object" "sample_dag" {
  name = "dags/tutorial2_dag.py"

  content = "${file("./dags/tutorial2_dag.py")}"
  bucket  = "${trimsuffix("${trimprefix("${local.dag_bucket}", "gs://")}", "/dags")}"
}