variable "project" {
  type = string
  description = "GCP Project ID"
}

variable "region" {
    type = string
    description = "The Region where to deploy resource"
}

variable "zone" {
    type = string
    description = "The zone where to deploy compute engine"
}

variable "db_instance_name" {
    type = string
    description = "DB instance name"
}

variable "database_version" {
    type = string
    description = "Database version to use for creating this instance"
}

variable "db_name" {
    type = string
    description = "Initial Database to crete in MySQL DB instance"
}

variable "labels" {
    type = map
    description = "User labels to be applied to all resources"
    default = {
        team = "analytics"
    }
}

variable "db_machine" {
    type = map
    description = "Database machine type to use and its configurations"
}