This project demonstrates how to use single metastore for two different Dataproc clusters.

The project can be deployed by issuing

```bash
gcloud init #choose the project that you will be deploying to
gcloud services enable dataproc.googleapis.com sqladmin.googleapis.com
export GCP_PROJECT=$(gcloud config get-value project)
gsutil mb gs://${GCP_PROJECT}-tf-state #terraform state bucket used as the back-end for the Google provider
terraform init
make apply
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
