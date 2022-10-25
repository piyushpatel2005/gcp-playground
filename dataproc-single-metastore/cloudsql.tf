resource "random_integer" "hive_metastore_number" {
  min = 10000
  max = 99999
}

data "google_secret_manager_secret_version" "creds" {
  secret = "db-credentials"
}

locals {
  db_creds = jsondecode(
    data.google_secret_manager_secret_version.creds.secret_data
  )
}

resource "google_sql_database_instance" "hive_metastore_instance" {
  region           = "${var.region}"
  name             = "${var.project}-hive-metastore-${random_integer.hive_metastore_number.result}"
  database_version = "${var.database_version}"
  deletion_protection = false

  settings {
    tier              = "db-n1-standard-1"
    activation_policy = "ALWAYS"

    location_preference {
      zone = "${var.zone}"
    }
  }
}

//Create a user because terraform deletes the default root user that comes with the mysql instance
resource "google_sql_user" "sql_user" {
  # name     = "root"
  name     = local.db_creds.username
  instance = "${google_sql_database_instance.hive_metastore_instance.name}"
  project  = "${var.project}"
  # password = "changeme"
  password = local.db_creds.password
  host     = "%"

  lifecycle {
    ignore_changes = [
      password,
    ]
  }
}
