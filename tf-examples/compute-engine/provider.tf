provider "google" {
    project = "<GCP_PROJECT_ID>"
    region = "us-west1"
    zone = "us-west1-a"
    credentials = "/path/to/credentials_file"
}

terraform {
  required_version = ">= 0.11.7"
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "4.57.0"
    }
    random = {
      source = "hashicorp/random"
      version = "3.4.3"
    }
  }
}
