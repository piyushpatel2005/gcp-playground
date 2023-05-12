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