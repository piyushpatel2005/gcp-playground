resource "random_id" "bucket_prefix" {
    byte_length = 16
}

resource "google_storage_bucket" "function_bucket" {
    name     = "${var.project_id}-function"
    location = var.region
    force_destroy = true
}

resource "google_storage_bucket" "input_bucket" {
    name     = "${var.project_id}-input"
    location = var.region
    force_destroy = true
}


# Generates an archive of the source code compressed as a .zip file.
data "archive_file" "source" {
    type        = "zip"
    source_dir  = var.source_dir
    output_path = var.output_path
}

# Add source code zip to the Cloud Function's bucket
resource "google_storage_bucket_object" "zip" {
    source       = data.archive_file.source.output_path
    content_type = "application/zip"

    # Append to the MD5 checksum of the files's content
    # to force the zip to be updated as soon as a change occurs
    name         = "src-${data.archive_file.source.output_md5}.zip"
    bucket       = google_storage_bucket.function_bucket.name

    # Dependencies are automatically inferred so these lines can be deleted
    depends_on   = [
        google_storage_bucket.function_bucket,  # declared in `storage.tf`
        data.archive_file.source
    ]
}

# Create the Cloud function triggered by a `Finalize` event on the bucket
resource "google_cloudfunctions_function" "function" {
    name                  = var.function_name
    runtime               = var.runtime  # of course changeable

    # Get the source code of the cloud function as a Zip compression
    source_archive_bucket = google_storage_bucket.function_bucket.name
    source_archive_object = google_storage_bucket_object.zip.name

    # Must match the function name in the cloud function `main.py` source code
    entry_point           = var.function_entry_point
    min_instances = var.min_instances
    max_instances = var.max_instances
    
    # Environment variables to be used in code
    environment_variables = {
      output_format = var.output_format
      project_id = var.project_id
      topic_name = var.topic_name
    }
    
    # Triggers
    event_trigger {
        event_type = "google.storage.object.finalize"
        resource   = "${var.project_id}-input"
    }

    # Dependencies are automatically inferred so these lines can be deleted
    depends_on            = [
        google_storage_bucket.function_bucket,  # declared in `storage.tf`
        google_storage_bucket_object.zip
    ]
}

###### Set up Topic and Subscription for real-time publishing ######
resource "google_pubsub_topic" "gpp_topic" {
  name = var.topic_name

  labels = {
    envirnoment = "sandbox"
  }

  message_retention_duration = "86600s"
}

resource "google_pubsub_subscription" "gpp_topic_subscription" {
    name = "${var.topic_name}-subscription"
    topic = google_pubsub_topic.gpp_topic.name
    
    ack_deadline_seconds = 15

    retry_policy {
      minimum_backoff = "5s"
    }
}