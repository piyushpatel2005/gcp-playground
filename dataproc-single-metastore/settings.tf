terraform {
  required_version = ">= 0.11.7"

  backend "gcs" {
    bucket = "dulcet-record-319917-tf-state"
    prefix = "terraform/state"
  }
}

provider "google" {
  project = "${var.project}"
  region  = "${var.region}"
}


