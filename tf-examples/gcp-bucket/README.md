# Running using Terraform

```shell
export PROJECT_ID=<PROJECT_ID>
# By default Terraform reads below variable for GCP credentials
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/json/keyfile
gcloud init
terraform init
terraform plan -var project=$PROJECT_ID
terraform apply -var project=$PROJECT_ID
terraform destroy -var project=$PROJECT_ID
terraform console -var project=$PROJECT_ID
```