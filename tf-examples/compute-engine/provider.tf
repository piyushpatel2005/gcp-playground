provider "google" {
    project = "playground-s-11-64478b9a"
    region = "us-west1"
    zone = "us-west1-a"
    credentials = "/Users/piyush/Downloads/playground-s-11-64478b9a-888aeb7da75d.json"
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
