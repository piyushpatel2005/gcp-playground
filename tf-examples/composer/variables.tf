variable "project" {
  type = string
}

variable "region" {
  type    = string
  default = "us-west1"
}

variable "database_version" {
  description = "The database version."
  default     = "MYSQL_5_7"
}

variable "zone" {
  type    = string
  default = "us-west1-a"
}

variable "location" {
  type    = string
  default = "US"
}

variable "storage_class" {
  type    = string
  default = "REGIONAL"
}

variable "machine_type" {
  type = string
  description = "The machine type for composer instance"
}

variable "db_machine_type" {
  type = string
  description = "Composer DB machine type"
}

variable "webserver_machine_type" {
  type = string
  description = "Composer webserver machine type"
}

variable "image_version" {
  type = string
  description = "Composer image version"
}

variable "labels" {
  type = object({
    environment = string
    team = string
  })
}