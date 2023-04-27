# Cloud SQL

Cloud SQL is a managed SQL database service on GCP. It offers MySQL, MSSQL or PostgreSQL databases. When creating an instance, you have to specify the root password, database version, whether it is production or development instance, single zone or multiple zones. We can also futher customize machine type, CPU, RAM etc.


```shell
gcloud auth login
gcloud config set account <PROJECT_ID>
gcloud auth list
gcloud auth revoke <email_account>
gcloud sql instances create mydb --database-version=MYSQL_8_0 --cpu 2 --memory 7680MB --region us-west1 
gcloud sql instances list
gcloud sql instances delete mydb
gcloud sql instances clone mydb anotherdb

# list datbases and create on above database instance
gcloud sql databases list --instance mydb
gcloud sql databases create dbname --instance mydb --charset utf8 --collation utf8_general_ci
gcloud sql databases describe dbname --instance mydb
gcloud sql databases delete dbname --instance mydb

```

```shell
export GOOGLE_PROJECT=<PROJECT_ID>
# By default Terraform reads below variable for GCP credentials
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/json/keyfile
gcloud init
terraform init
terraform plan -var project=$GOOGLE_PROJECT
terraform apply -var project=$GOOGLE_PROJECT
terraform destroy -var project=$GOOGLE_PROJECT
terraform console -var project=$GOOGLE_PROJECT
```

## Instructions for Windows Command Prompt

You may need to set up provider.tf file to configure the google provider defaults

```terraform-ls
provider "google" {
    project = "GCP_PROJECT_ID"
    region = "DEFAULT_REGION"
    credentials = "C:\\path\\to\\credential_file
}
```

```cmd
set GOOGLE_PROJECT=<PROJECT_ID>
set GOOGLE_APPLICATION_CREDENTIALS=C:\\path\\to\\json_file
terraform init
terraform plan -var project=%PROJECT_ID%
terraform apply -var project=%PROJECT_ID%
terraform destroy -var project=%PROJECT_ID%
terraform console -var project=%PROJECT_ID%
```