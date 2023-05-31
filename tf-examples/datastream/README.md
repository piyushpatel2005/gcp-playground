# Datastream

Datastream is serverless and easy to use CDC and replicatio nservice that allows to synchronize data across various databases, storage systems and applications reliably and with minimum latency. This service also supports streaming data changes into Cloud storage.

Datastream also allows for private connection between Google cloud and customer's network.
To connect to mysql from cloud storage, use `gcloud sql connect <instance-name> --user=root`. After IP allow whitelist, it will prompt for the password of `root` user.

For connecting to any database instance, the first step is to create Connection Profile for a given database. For this, the database instance should allow network which has the IP ranges specified in the IP allowlist of GCP. Similarly, create destination connection profile.

Next step is to setup the Stream where we specify source connection, destination connection and type of replication. For this to work, the database instance needs to have binary logging enabled so that we can stream binlog information.

For Datastream connection profile, we have set up user `user1`  with random password. In order to view the password run, `terraform output db_password`. There is also flexibility to specify which columns or schemas or tables we want to import to destination. The destination can be GCS or BigQuery or even another database instance. For better control, the binlogs could be written to GCS location from where Dataflow job may read and process with custom processing logic and write to any output destination.


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
export PASSWORD=<PASSWORD>
gcloud init
terraform init
terraform plan -var project=$GOOGLE_PROJECT -var sql_password=$PASSWORD
terraform apply -var project=$GOOGLE_PROJECT -var sql_password=$PASSWORD
# After running this, from Cloud SQL instance page, we have to import data.sql from GCS bucket to load some dummy data.
terraform destroy -var project=$GOOGLE_PROJECT -var sql_password=$PASSWORD
terraform console -var project=$GOOGLE_PROJECT -var sql_password=$PASSWORD
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
set PASSWORD=<PASSWORD>
terraform init
terraform plan -var project=%PROJECT_ID%
terraform apply -var project=%PROJECT_ID%
terraform destroy -var project=%PROJECT_ID%
terraform console -var project=%PROJECT_ID%
```