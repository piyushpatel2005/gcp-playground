variable "project" {
  type = string
  default = "dulcet-record-319917"
}

variable "region" {
  type    = string
  default = "northamerica-northeast1"
}

variable "database_version" {
  description = "The database version."
  default     = "MYSQL_5_7"
}

variable "zone" {
  type    = string
  default = "northamerica-northeast1-a"
}

variable "location" {
  type    = string
  default = "US"
}

variable "storage_class" {
  type    = string
  default = "MULTI_REGIONAL"
}

variable "data_directory" {
  type    = string
  default = "./data"
}

variable "state_bucket" {
  type    = string
  default = "dulcet-record-319917-tf-state"
}

variable "scripts_directory" {
  type = string
  description = "The scripts directory to upload to GCP"
  default = "./scripts"
}