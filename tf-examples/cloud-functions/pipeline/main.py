import argparse
import time
import logging
import json
import typing
from datetime import datetime
import apache_beam as beam
from apache_beam.options.pipeline_options import GoogleCloudOptions
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import StandardOptions
from apache_beam.transforms.combiners import CountCombineFn
from apache_beam.runners import DataflowRunner, DirectRunner
from utils import output_schema

# ### functions and classes

class JsonData(typing.NamedTuple):
    file_format_version: str
    vendor_name: str
    dn_prefix: float
    local_dn: float
    element_type: str
    begin_time: str
    end_time: int
    me_local_dn: int
    user_label: str
    sw_version: str
    meas_info_id: str
    jobid: str
    granp_duration: str
    granp_end_time: str
    rep_duration: str
    attTCHSeizures: str
    succTCHSeizures: str
    attImmediateAssignProcs: str
    succImmediateAssignProcs: str
    meas_obj_ldn: str
    input_file: str
    input_datetime: str

beam.coders.registry.register_coder(CommonLog, beam.coders.RowCoder)

def parse_json(element):
    row = json.loads(element.decode('utf-8'))
    return JsonData(**row)

def add_processing_timestamp(element):
    row = element._asdict()
    row['event_timestamp'] = row.pop('timestamp')
    row['processing_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return row

class GetTimestampFn(beam.DoFn):
    def process(self, element, window=beam.DoFn.WindowParam):
        window_start = window.start.to_utc_datetime().strftime("%Y-%m-%dT%H:%M:%S")
        output = {'page_views': element, 'timestamp': window_start}
        yield output

# ### main

def run():
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input_subscription",
        help='Input PubSub subscription of the form "projects/<PROJECT>/subscriptions/<SUBSCRIPTION>."',
    )
    parser.add_argument(
        "--output_table",
        help="Output BigQuery Table, e.g. PROJECT_ID:DATASET_NAME.TABLE_NAME",
    )
    parser.add_argument(
        "--output_schema",
        help="Output BigQuery Schema in text format, e.g. timestamp:TIMESTAMP,attr1:FLOAT,msg:STRING",
    )
    parser.add_argument(
        "--machine_type",
        help="Machine instance type",
        default="e2-medium",
    )
    parser.add_argument(
        "--disk_size_gb",
        help="Worker disk size",
        default=30,
    )
    parser.add_argument(
        "--max_num_workers",
        help="Maximum count of workers",
        default=1,
    )
    parser.add_argument(
        "--use_public_ips",
        help="Enable public ip addresses",
        default=False,
    )
    known_args, pipeline_args = parser.parse_known_args()

    # See https://cloud.google.com/dataflow/docs/reference/pipeline-options
    pipeline_options = PipelineOptions(
        pipeline_args,
        runner='DataflowRunner',
        max_num_workers=known_args.max_num_workers,
        num_workers=1,
        disk_size_gb=known_args.disk_size_gb,
        machine_type=known_args.machine_type,
        use_public_ips=known_args.use_public_ips
    )
    pipeline_options.view_as(StandardOptions).streaming = True


    # Create the pipeline
    p = beam.Pipeline(options=pipeline_options)



    parsed_msgs = (p | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(subscription=known_args.input_subscription, timestamp_attribute=None)
                     | 'ParseJson' >> beam.Map(parse_json).with_output_types(JsonData))

    (parsed_msgs
        | 'WriteRawToBQ' >> beam.io.WriteToBigQuery(
            known_args.output_table,
            schema=output_schema,
            create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED,
            write_disposition=beam.io.BigQueryDisposition.WRITE_APPEND
            )
        )


    logging.getLogger().setLevel(logging.INFO)
    logging.info("Building pipeline ...")

    p.run().wait_until_finish()

if __name__ == '__main__':
  run()