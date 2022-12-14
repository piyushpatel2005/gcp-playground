# GCP Playground and experiments

The purpose of this is to play with GCP and learn and configure different aspects of GCP.

## Prerequisites

1. Install Gcloud CLI
2. Create Google cloud account and enable Cloud Dataproc API.

## Installations

```shell
# google-cloud-sdk
sudo apt-get install apt-transport-https ca-certificates gnupg
echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
sudo apt-get update && sudo apt-get install google-cloud-cli
gcloud --help
gcloud init
# terraform
sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor | \
    sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" | \
    sudo tee /etc/apt/sources.list.d/hashicorp.list
sudo apt update && sudo apt-get install terraform
terraform --help
```

## Deploy Dataproc cluster using gcloud command

```shell
# First make sure you enable services on GCP.
gcloud enable <servicename> # servicename can be found from  UI
gcloud enable staroge.googleapis.com
```