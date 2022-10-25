resource "google_storage_bucket" "warehouse" {
  name     = "${var.project}-warehouse"
  location = "${var.location}"
  project  = "${var.project}"
  force_destroy = "true"
}

resource "google_storage_bucket" "hive_metastore_state_data_artif_bucket" {
  name          = "${var.project}-artif"
  location      = "${var.location}"
  project       = "${var.project}"
  storage_class = "${var.storage_class}"
  force_destroy = "true"
}

resource "google_storage_bucket_object" "cloud_sql_proxy_script" {
  name = "dataproc/cloud-sql-proxy.sh"

  content = "${file("./scripts/cloud-sql-proxy.sh")}"
  bucket  = "${google_storage_bucket.hive_metastore_state_data_artif_bucket.name}"
}

resource "null_resource" "upload_data_folder" {
  triggers = {
    file_hashes = jsonencode({
      for fn in fileset(var.data_directory, "**"):
        fn => filesha256("${var.data_directory}/${fn}")
    })
  }

  provisioner "local-exec" {
    command = "gsutil cp -r ${var.data_directory}/* gs://${var.state_bucket}/data/"
  }
}

resource "null_resource" "upload_scripts_folder" {
  triggers = {
    file_hashes = jsonencode({
      for fn in fileset(var.scripts_directory, "**"):
        fn => filesha256("${var.scripts_directory}/${fn}")
    })
  }

  provisioner "local-exec" {
    command = "gsutil cp -r ${var.scripts_directory}/* gs://${var.state_bucket}/scripts/"
  }
}