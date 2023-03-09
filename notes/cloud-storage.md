# Google Cloud Storage (GCS)

- Distributed object storage (NOT A FILE SYSTEM). We cannot write a file, we can upload or download.


## Tools for Access

1. Console
2. GCloud CLI with `gcloud storage`
3. Client libraries for programmatic access
4. REST API for making requests using REST calls.
5. Terraform for declarative configuration management

Some of the key features:

- Control to Bucket is provided using IAM permissions or object level permissions using ACLs (legacy). With IAM permissions also we can provide object level permissions by specifying pattern of objects.
- Data encryption using Google managed key or customer supplied encryption keys
- The access can be authenticated using multiple methods OAuth, gstil, API authentication, etc.
- Bucket lock and bucket retention to define when to remove a bucket after certain time or limit anyone from accidentally deleting an object.
- Object versioning to have multiple versions of the bucket for certain time period for data recovery.

```shell
# Initialize the gcloud cli, works directly if on Cloud shell
gcloud init
# Create bucket using gsutil
gsutil mb <bucket_name>
gsutil ls <bucket_name>
gsutil rm <bucket_name>/<object_name>
gsutil rm <bucket_name>/<object_name>
gsutil cp gs://<bucket_name>/<dir_name>/ gs://<another_bucket>/<dir_name>/ # If there is single file, it will not go in the correct directory
# To move many files in parallel use -m flag.
gsutil -m mv gs://<bucket_name>/<dir_name>/ gs://<another_bucket>/<dir_name>/
# Get help using
gsutil --help
# Get help for specific command
gsutil mv --help



# Another option using gcloud storage commands
gcloud storage buckets create gs://<bucket_name>
gcloud storage ls gs://<bucket_name>
gcloud storage cat gs://<bucket_name>/<object_name>
gcloud storage cp test.txt gs://<bucket_name>
gcloud storage buckets --help
gcloud storage buckets describe gs://<bucket_name>
gcloud storage buckets update gs://<bucket_name>
# set retention period or modify
gcloud storage buckets update gs:/<bucket_name> --retention-period=2y180d
# enable versioning
gcloud storage buckets update gs://<bucket_name> --versioning
# disable versioning
gcloud storage buckets update gs://<bucket_name> --no-versioning
# storage buckets options
gcloud storage buckets add-iam-policy-binding|create|delete|describe|get-iam-policy|list|update|set-iam-policy|remove-iam-policy-binding
# gcloud storage objects options
gcloud storage objects --help
gcloud storage objects compose | describe | list | update
# compose or concatenate object1 and object2 to new object3
gcloud storage objects compose gs://<bucket>/object1 gs://<bucket>/object2 gs://<bucket>/object3
```

## Permissions and In-built roles

Cloud storage permissions are assigned using roles in GCP. There are few general-purpose built-in roles available in GCP which can be useful to provide permissions in most case. The documentation for that can be found [here](https://cloud.google.com/storage/docs/access-control/iam-roles). The detailed information about each of the permissions assigned to those roles are mentioned [here](https://cloud.google.com/storage/docs/access-control/iam-permissions)

## Creating buckets using Terraform and retrieving information

```shell
cd tf-examples/gcp-bucket
export PROJECT_ID=<PROJECT_ID>
# By default Terraform reads below variable for GCP credentials
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/json/keyfile
gcloud init
terraform init
terraform plan -var project=$PROJECT_ID
terraform apply -var project=$PROJECT_ID
terraform destroy -var project=$PROJECT_ID
terraform console -var project=$PROJECT_ID
````