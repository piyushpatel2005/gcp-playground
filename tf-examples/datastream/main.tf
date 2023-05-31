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
  name             = var.db_instance_name
  database_version = var.database_version
  region           = var.region

  settings {
    tier = "db-${var.db_machine.type}"

    ip_configuration {
      # ipv4_enabled                                  = true
      # private_network                               = google_compute_network.vpc_network.id
      # enable_private_path_for_google_cloud_services = true
      # authorized_networks {
      #   name = "all-ips"
      #   value = "0.0.0.0/0"
      # }

      dynamic "authorized_networks" {
        for_each = data.google_datastream_static_ips.datastream_ips.static_ips
        iterator = ip

        content {
          value = ip.value
        }
      }
    }

    backup_configuration {
      enabled            = true
      binary_log_enabled = true
    }
  }

  deletion_protection = "false"
}

resource "google_sql_database" "database" {
  name       = var.db_name
  instance   = google_sql_database_instance.master.name
  charset    = "utf8"
  collation  = "utf8_general_ci"
  depends_on = [google_sql_database_instance.master]
}

resource "google_sql_user" "users" {
  name       = "root"
  instance   = google_sql_database_instance.master.name
  host       = "%"
  password   = var.sql_password
  depends_on = [google_sql_database_instance.master]
}

# SQL Data
# resource "google_sql_source_representation_instance" "instance" {
#   name             = "${var.db_name}-data"
#   region           = var.region
#   database_version = var.database_version
#   host             = google_sql_database_instance.master.public_ip_address
#   port             = 3306
#   username         = "root"
#   password         = var.sql_password
#   dump_file_path   = "gs://${google_storage_bucket.data_bucket.name}/mysql/data.sql"
#   depends_on = [
#     google_sql_database.database,
#     google_storage_bucket_object.data_file
#   ]
# }

resource "google_storage_bucket" "data_bucket" {
  project       = var.project
  name          = var.project
  location      = var.region
  storage_class = "STANDARD"

  uniform_bucket_level_access = true
}

resource "google_storage_bucket_object" "data_file" {
  name   = "mysql/data.sql"
  source = "./data.sql"
  bucket = google_storage_bucket.data_bucket.name
}

# Get Datastream public IPs for this region
data "google_datastream_static_ips" "datastream_ips" {
  location = var.region
  project  = var.project
}

output "ip_list_us_west1" {
  value = data.google_datastream_static_ips.datastream_ips.static_ips
}

# MySQL connection profile
resource "random_password" "pwd" {
  length  = 16
  special = false
}

resource "google_sql_user" "user" {
  name     = "user1"
  instance = google_sql_database_instance.master.name
  password = random_password.pwd.result
}

output "db_password" {
  value     = random_password.pwd.result
  sensitive = true
}

resource "google_datastream_connection_profile" "mysql_profile" {
  display_name          = "MySQL Datastream Connection"
  location              = var.region
  connection_profile_id = "mysql_datastream_profile"

  # postgresql_profile {
  #     hostname = google_sql_database_instance.master.public_ip_address
  #     username = google_sql_user.user.name
  #     password = google_sql_user.user.password
  #     database = google_sql_database.database.name
  # }

  mysql_profile {
    hostname = google_sql_database_instance.master.public_ip_address
    username = google_sql_user.user.name
    password = google_sql_user.user.password
  }
}

resource "google_datastream_connection_profile" "bigquery_profile" {
  display_name          = "BigQuery Datastream Connection"
  location              = var.region
  connection_profile_id = "bigquery_datastream_profile"

  bigquery_profile {
  }
}

# Datastream set up
resource "google_datastream_stream" "default"  {
    display_name = "MySQL to BigQuery"
    location     = var.region
    stream_id    = "mysql-bigquery-stream"
    desired_state = "RUNNING"

    source_config {
        source_connection_profile = google_datastream_connection_profile.mysql_profile.id
        mysql_source_config {
          max_concurrent_cdc_tasks = 2
          include_objects {
            mysql_databases {
              database = "customers"
              mysql_tables {
                table = "customers"
                # mysql_columns {
                #   column = "customerNumber"
                #   primary_key = true
                # }
                # mysql_columns {
                #   column = "customerName"
                # }
                # mysql_columns {
                #   column = "city"
                # }
              }
            }
          }
          # exclude_objects {

          # }
        }
        # postgresql_source_config {
        #     max_concurrent_backfill_tasks = 12
        #     publication      = "publication"
        #     replication_slot = "replication_slot"
        #     include_objects {
        #         postgresql_schemas {
        #             schema = "schema"
        #             postgresql_tables {
        #                 table = "table"
        #                 postgresql_columns {
        #                     column = "column"
        #                 }
        #             }
        #         }
        #     }
        #     exclude_objects {
        #         postgresql_schemas {
        #             schema = "schema"
        #             postgresql_tables {
        #                 table = "table"
        #                 postgresql_columns {
        #                     column = "column"
        #                 }
        #             }
        #         }
        #     }
        # }
    }

    destination_config {
        destination_connection_profile = google_datastream_connection_profile.bigquery_profile.id
        bigquery_destination_config {
            data_freshness = "900s"
            source_hierarchy_datasets {
                dataset_template {
                   location = var.region
                }
            }
        }
    }

    # backfill_all {
    #     postgresql_excluded_objects {
    #         postgresql_schemas {
    #             schema = "schema"
    #             postgresql_tables {
    #                 table = "table"
    #                 postgresql_columns {
    #                     column = "column"
    #                 }
    #             }
    #         }
    #     }
    # }
    backfill_all {
      
    }
}