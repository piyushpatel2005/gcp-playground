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
    dn_prefix: str
    local_dn: str
    element_type: str
    begin_time: str
    end_time: str
    me_local_dn: str
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
    input_date_time: str
    transformed_file: str

    def __str__(self):
        return f"JsonData({self.file_format_version}, {self.begin_time}, {self.granp_duration}, {self.granp_end_time}, {self.attImmediateAssignProcs}, {self.attTCHSeizures}, {self.succImmediateAssignProcs}, {self.succTCHSeizures}, {self.meas_info_id}, {self.meas_obj_ldn})"

beam.coders.registry.register_coder(JsonData, beam.coders.RowCoder)

class ConvertToJsonDataFn(beam.DoFn):
  def process(self, element):
    try:
        row = json.loads(element.decode('utf-8'))
        yield beam.pvalue.TaggedOutput('parsed_row', JsonData(**row))
    except:
        yield beam.pvalue.TaggedOutput('unparsed_row', element.decode('utf-8'))

def parse_json(element):
    row = json.loads(element.decode('utf-8'))
    # row = json.loads(element)
    return JsonData(**row)

def print_row(row):
    del row['transformed_file']
    logging.info(row)

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
        "--input_topic",
        help='Input Pubsub Topic of the form projects/<PROJECT_ID>/topics/<TOPIC>'
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



    parsed_msgs = (p 
                   # | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(subscription=known_args.input_subscription, timestamp_attribute=None)
                   | 'ReadFromPubSub' >> beam.io.ReadFromPubSub(topic=known_args.input_topic)
                   | 'ParseJson' >> beam.Map(parse_json).with_output_types(JsonData)
                   # | 'ParseJson' >> beam.ParDo(ConvertToJsonDataFn()).with_outputs('parsed_row', 'unparsed_row').with_output_types(JsonData)
                   )


    (parsed_msgs
     | 'ConsoleOutput' >> beam.Map(print_row))
    
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