variable "project" {
  type = string
  description = "GCP Project ID"
}

variable "region" {
    type = string
    description = "The Region where to deploy resource"
    default = "us-west1"
}