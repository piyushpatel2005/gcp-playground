This project demonstrates how to use single metastore for two different Dataproc clusters.

The project can be deployed by issuing

```bash
gcloud init #choose the project that you will be deploying to
gcloud services enable dataproc.googleapis.com sqladmin.googleapis.com
export GCP_PROJECT=$(gcloud config get-value project)
gsutil mb gs://${GCP_PROJECT}-tf-state #terraform state bucket used as the back-end for the Google provider
sed -i "s/TF_BACKEND/${GCP_PROJECT}-tf-state/" settings.tf
terraform init
```

Create Google secret with following pattern.

```json
{
   "username": "root",
   "password": "changeme"
}
```

```shell
# These are going to be used for Metastore
export SQL_USERNAME=USERNAME
export SQL_PASSWORD=PASSWORD
sed -i "s/SQL_ADMIN_USERNAME/${SQL_USERNAME}/" scripts/cloud-sql-proxy.sh
sed -i "s/SQL_ADMIN_PASSWORD/${SQL_PASSWORD}/" scripts/cloud-sql-proxy.sh
TF_VAR_project=$GCP_PROJECT terraform plan # verify configs or alternatively
terraform plan -var "project=${GCP_PROJECT}"
terraform apply -var "project=${GCP_PROJECT}"
```

and destroy using
```bash
make destroy
```

--- 

To generate a graph displaying all the resources in this terraform project run

```bash
docker build -t graphwiz . &&
   terraform graph -type=plan > graph.dot &&
   docker run -v $(PWD):/tmp graphwiz dot /tmp/graph.dot -Tpng -o /tmp/graph.png &&
   rm graph.dot
```
