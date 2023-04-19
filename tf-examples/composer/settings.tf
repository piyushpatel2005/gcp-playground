locals {
  project = "${var.project}"
}

terraform {
  required_version = ">= 0.11.7"

  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.57.0"
    }
  }
}

provider "google" {
  project = var.project
  region = var.region
  zone = var.zone
  credentials = file("credentials.json")
}


