# Creating and Managing tables using Python Client Libraries

Enable BigQuery API from Enable API and Services.

In order to use this API, we need to be authenticated using [Application Default credentials](https://cloud.google.com/docs/authentication/application-default-credentials). It works as below. All client libraries searches below locations to find application default credentials (ADC).

1. `GOOGLE_APPLICATION_CREDENTIALS` environment variable which provides the location of the JSON credentials file.
2. User credentials set up by Google Cloud CLI. This is set using `gcloud auth application-default login`. It stores the credentials file under `$HOME/.config/gcloud/application_default_credentials.json`.
3. The attached service account returned by metadata server. Many cloud services let you attach a service account that can be used to provide credentials for accessing GCP APIs. Using the credentials from the attached service account is the preferred method for finding credentials in a production environment. In this, we create service account and assign certain permissions on service account. If we want to set up local development environment using that service account, we can impersonate using that service account using command `gcloud auth application-default login --impersonate-service-account <service_account_email>`. In order to impersonate, the user must have `roles/iam.serviceAccountTokenCreator` role on the service account. This can be provided using IAM > Service Accounts > Select service account > Permissions > Grant Access > Provide Principal email > Roles > Service Account Token Creator > Save.

