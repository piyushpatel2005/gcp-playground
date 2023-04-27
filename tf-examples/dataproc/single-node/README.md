```shell
# Enable Cloud Resource Manager API
# also ensure that the default compute service account has the Cloud Storage Admin access for staging and temp buckets
terraform init
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

```cmd
set GOGOLE_PROJECT=<PROJECT_ID>
set GOOGLE_APPLICATION_CREDENTIALS=C:\\path\\to\\json\\credentials
terraform init 
terraform plan -var project_id=%GOOGLE_PROJECT%
terraform apply -var project_id=%GOOGLE_PROJECT%
terraform destroy -var project_id=%GOOGLE_PROJECT%
```.0


Each Dataproc cluster contains, hadoop-gcs-connector located under `usr/local/share/google/dataproc/lib` directory. Due to this, copying data to GCS using distcp command will be seamless.
To distcp some data from HDFS to GCS is very straight forward, `hadoop distcp hdfs://tmp/hive/_resultscache_ gs://essential-oven-380216/`

