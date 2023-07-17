# Create new storage bucket in the US multi-region
# with coldline storage
resource "random_id" "bucket_prefix" {
    byte_length = 16
}

resource "google_storage_bucket" "static" {
    project       = var.project
    name          = "${random_id.bucket_prefix.hex}-new-bucket"
    location      = "US"
    storage_class = "COLDLINE"

    uniform_bucket_level_access = true

# Prevent bucket from deletion
#   lifecycle {
#     prevent_destroy = true
#   }
}

# Upload files
# Discussion about using tf to upload a large number of objects
# https://stackoverflow.com/questions/68455132/terraform-copy-multiple-files-to-bucket-at-the-same-time-bucket-creation

# The text object in Cloud Storage
resource "google_storage_bucket_object" "default" {
    name = "new-object"
    # Uncomment and add valid path to an object.
    # One of content or source should be specified, not both
    #    source       = "/path/to/an/object"
    content      = "Data as string to be uploaded"
    content_type = "text/plain"
    bucket       = google_storage_bucket.static.id
}
