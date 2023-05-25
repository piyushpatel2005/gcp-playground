provider "google" {
  project     = var.project_id
  region      = var.region
  zone        = var.zone
  credentials = file("credentials.json")
}

provider "google-beta" {
  project = var.project_id
  region = var.region
  zone = var.zone
  credentials = file("credentials.json")
}

terraform {
  required_version = ">= 0.11.7"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.57.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.4.3"
    }
  }
}
