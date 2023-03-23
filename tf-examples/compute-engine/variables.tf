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
    description = "The zone where to deploy compute engine"
    default = "us-west1-a"
}

variable "tags" {
    type = map
    description = "Tags to be applied to all resources"
    default = {
        subgroup = "analytics"
        # team = "datascience" # variables take precedence because that gets applied in merge later
    }
}