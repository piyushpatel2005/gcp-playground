variable "project" {
  type = string
  description = "GCP Project ID"
}

variable "region" {
    type = string
    description = "The Region where to deploy resource"
    default = "us-west1"
}

variable "zone" {
  type = string
  description = "The default zone"
  default = "us-west1-a"
}