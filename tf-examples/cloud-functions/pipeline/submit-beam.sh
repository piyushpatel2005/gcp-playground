export PROJECT_ID=$(gcloud config get-value project)
export REGION="us-west1"
export BUCKET=gs://${PROJECT_ID}
export PIPELINE_FOLDER=${BUCKET}
export RUNNER=DataflowRunner
export PUBSUB_TOPIC=projects/${PROJECT_ID}/topics/gpp-topic
export PUBSUB_SUBSCRIPTION=projects/${PROJECT_ID}/subscriptions/gpp-topic-subscription
export WINDOW_DURATION=60
export ALLOWED_LATENESS=1
export OUTPUT_TABLE_NAME=${PROJECT_ID}:ericsson_expl.ran_tbl
export DEADLETTER_BUCKET=${BUCKET}
BASE_DIR=$PWD
cd $BASE_DIR
gsutil mb $BUCKET
python3 main.py \
--project=${PROJECT_ID} \
--region=${REGION} \
--staging_location=${PIPELINE_FOLDER}/staging \
--temp_location=${PIPELINE_FOLDER}/temp \
--runner=${RUNNER} \
--requirements_file requirements.txt \
--input_topic=${PUBSUB_TOPIC} \
--input_subscription=${PUBSUB_SUBSCRIPTION} \
--window_duration=${WINDOW_DURATION} \
--allowed_lateness=${ALLOWED_LATENESS} \
--table_name=${OUTPUT_TABLE_NAME} \
--output_table=${OUTPUT_TABLE_NAME} \
--dead_letter_bucket=${DEADLETTER_BUCKET} \
--allow_unsafe_triggers