# Cloud Functions

Cloud functions provide service Function as a Service (FaaS). This is serverless and there is no infrastructure to manage. Functions are billed per 100 millisecond and by default 200 million monthly invocations are free, i.e. 20 million seconds of executions.

## Local Development

There are two main types of functions. (1) HTTP functions (2) Event-driven functions
For local development, functions can run locally, either using Functions Framework or Cloud Native buildpacks.
1. Functions Framework: open-source libraries to unmarshal incoming HTTP requests into language-specific function invocations. This can be used to convert function into locally-runnable HTTP service. This has lower resource needs and do not require underlying containerzation software. However, this require underlying language infrastructure (package manager and language runtimes).
2. Cloud Native buildpacks are used to wrap HTTP services created by Functions framework into runnable Docker containers.

### Python Example:

```shell
pip install functions-framework
```

For functions, below configs can be edited `--port` or environment variable `PORT` on which to listen requests (default 8080), `--target` or `FUNCTION_TARGET` is the name of the exported function to be invoked, default is `function`. `--signature-type` or `FUNCTION_SIGNATURE_TYPE` is the signature type used by the function. This can be *http* (default), *event* or *cloudevent*. To run the function, we invoke using `functions-framework --target=<fn_name>`

```shell
cd examples/local_dev
functions-framework --target=hello_world
# Enter url http://localhost:8080?name=there
```

To call function on Google use `gcloud functions call <function_name> --data '{"name": "Someone"}'`
We can also test PubSub functions using PubSub Emulator with buildpacks.

```shell
# Deploying cloud function
terraform init
terraform plan -var project_id=$GOOGLE_PROJECT
terraform apply -var project_id=$GOOGLE_PROJECT
terraform destroy -var project_id=$GOOGLE_PROJECT
```

You can set up Cloud Functions to execute in response to various scenario specifying a trigger for your function. Triggers can be HTTP request or one of the number of supported events as mentioned in [Triggers supported in Cloud functions](https://cloud.google.com/functions/docs/calling). When using HTTP trigger, the function is assigned a URL at which it can receive requests. By default, requests to a function with an HTTP triggere require authentication.

```shell
gcloud services list --available
gcloud services enable run.googleapis.com
# allow-unauthenticated : function can be called without authentication
gcloud functions deploy <function_name> \
--trigger-http \
--allow-unauthenticated \
--security-level=<SECURITY_LEVEL> # secure-always: HTTPS, secure-optional: HTTP or HTTPS

# Get URL for Trigger (2nd Gen)
gcloud functions describe <fuction_name> gen2 --region=<REGION> --format="value(httpsTrigger.url)"

gcloud functions deploy <function_name> \
[--gen2] --region=<REGION> \
--runtime=<runtime> \
--source=<source_directory> \
--entry-point=<function-entry-point>
<TRIGGER-FLAGS>
# Trigger flags can be --trigger-http, --trigger-bucket=<bucket>, --trigger-event-filters=<event>, --trigger-event=<event-type>

gcloud functions deploy http-simple-function --trigger-http --gen2 --region=us-west1 --runtime=python38 --source=./local_dev --entry-point=hello_world

gcloud functions delete http-simple-function --region=us-west1
gcloud functions describe http-simple-function --region=us-west1

# To set environment variables to be used in the code using os.environ.get()
gcloud functions deploy <fn-name> --set-env-vars FOO=bar ...
```

## Best Practices:

1. Write idempotent functions that produce the same result even if they are called multiple times.
2. Do not start background processes with function calls.
3. Always delete temporary files. If files are not deleted, they consume memory available to the function and sometimes persist between invocations. Do not attempt to write outside of the temporary directory. The memory footprint can be reduced by processing larger file susing pipelining. Create a read stream, pass through stream process and write output stream directly to Cloud Storage.
4. Do not use `sys.exit()` for exiting in the middle of execution.
5. For sending email from Cloud function, use SendGrid as it does not allow outbound connections on port 25.
6. Reduce cold starts by setting a minimum number of instances. By default, Cloud functions scales the number of instances based on the number of requests. This can be changed by setting the number of instances that Cloud functions must keep ready to serve requests. This is great for applications which are latency-sensitive.