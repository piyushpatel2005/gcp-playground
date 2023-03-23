# Running using Terraform

In this one, we will store the Terraform state in GCP cloud storage. In order to do that, it needs to have bucket create, list and object get, create, update, delete permissions.

1. First have the section of the code which will create the bucket with random prefix and create that bucket using terraform commands.
2. Set the bucket name in the `backend.tf` file to use that bucket for backend.

Terraform by default reads few environment variables to set the permissions for Terraform commands. For example, `GOOGLE_APPLICATION_CREDENTIALS` for credentials file path, `GOOGLE_PROJECT` for default Google project ID.

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

Alternatively, we can configure google provider with project information and the credentials information in order to be able to by default provide those in all resource definitions.

```golang
provider "google" {
    project = "<GCP_PROJECT>"
    region = "us-west1"
    zone = "us-west1-a"
    credentials = "<PATH_TO_JSON_CREDENTIALS_FILE>"
}
```

For Terraform, we can specify exact version of the terraform provider plugin. If we update the version of provider plugin, then we have to re-initialize plugins using `terraform init -upgrade`. These are downloaded into `.terraform` directory.
For different environments, we can different variable files which will hold the variable values, like `staging.tfvars` or `prod.tfvars`. To reference those files for each environment, we can use the command `terraform apply -var-file="prod.tfvars"`. If we don't use `-var-file` option, by default `terraform.tfvars`  file will be used as a variable file.

The `output` block can be used to output any specific attribute value of a resource. The available attributes can be found in official provider documentation under *Attribute Reference* section.
To hide sensitive information, we can use `sensitive = true` in the output declaration. This will avoid displaying those output unless explicitly invoked using `terraform output <output_name>`