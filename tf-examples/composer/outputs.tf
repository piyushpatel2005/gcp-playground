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
