project_id = "essential-oven-380216"
region = "us-west1"
zone = "us-west1a"
function_name = "function-trigger-on-gcs"
runtime = "python310"
# function_entry_point = "hello_gcs"
function_entry_point = "lambda_handler"
# source_dir = "./examples/demo_event_fn"
source_dir = "./3gpp_fn"
output_path = "./tmp/function.zip"
topic_name = "gpp-topic"
output_format = "json"
bigquery_dataset = "ericsson_expl"
bigquery_table = "ran_tbl"