from google.cloud import storage
import logging
import datetime
import xml.etree.ElementTree as ET
import xmltodict
import json
import csv
import time
import os
import sys
from GPPXmlFlat import GPPXmlFlat
from google.cloud import pubsub_v1

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def write_to_json(records, out_fname):
    with open(out_fname, 'w') as file_json:
        for rec in records:
            file_json.write(json.dumps(rec) + "\n")

    return None

def publish_to_pubsub(records, publisher, topic_name):
    project = os.environ['project_id']
    topic_path = publisher.topic_path(project, topic_name)
    print('Project : ', project)
    print('Topic path : ', topic_path)
    for record in records:
        json_record = json.dumps(record)
        message_bytes = json_record.encode('utf-8')
        try:
            publish_future = publisher.publish(topic_path, data=message_bytes)
            publish_future.result()
            # return 'Published'
        except Exception as e:
            print(e)
            return (e, 500)


def write_to_csv(header, records, out_fname):
    with open(out_fname, 'w', encoding='utf8', newline='') as file_csv:
        fc = csv.DictWriter(file_csv,
                            fieldnames=header,
                            delimiter='|',
                            lineterminator='\n')
        fc.writeheader()
        fc.writerows(records)

    return None


def lambda_handler(event, context):
    bucket = event['bucket']
    key = event['name']
    event_type = context.event_type

    fname = key.split('/')[-1].split('.')[0]

    output_format = os.environ['output_format'].upper()

    tmp_out_dir = '/tmp'

    fprefix = str(int(round(time.time() * 1000)))
    tmp_xml_file = tmp_out_dir + '/' + fprefix + '_' + fname + '.xml'

    if output_format == 'JSON':
        tmp_out_fname = fprefix + '_' + fname + '.json'
        out_transform_prefix = 'raw_transform_json'
    elif output_format == 'CSV':
        tmp_out_fname = fprefix + '_' + fname + '.csv'
        out_transform_prefix = 'raw_transform_csv'
    else:
        raise

    tmp_out_file = tmp_out_dir + '/' + tmp_out_fname

    # logger.info("Event : ", event)
    # logger.info("type(event) : ", type(event))
    # logger.info("In GCS bucket : ", bucket)
    # logger.info("GCS Key : ", key)
    # logger.info("Event type : ", event_type)
    # logger.info("Output Format   : " + output_format)
    # logger.info("Temp out dir    : " + tmp_out_dir)
    # logger.info("Temp out fname  : " + tmp_out_fname)
    # logger.info("File Name       : " + fname)
    # logger.info("Out File Prefix : " + fprefix)
    # logger.info("Temp XML file   : " + tmp_xml_file)
    # logger.info("Temp OUT file   : " + tmp_out_file)
    # logger.info("Out GCS Prefix   : " + out_transform_prefix)

    print("Event : ", event)
    print("type(event) : ", type(event))
    print("In GCS bucket : ", bucket)
    print("GCS Key : ", key)
    print("Event type : ", event_type)
    print("Output Format   : " + output_format)
    print("Temp out dir    : " + tmp_out_dir)
    print("Temp out fname  : " + tmp_out_fname)
    print("File Name       : " + fname)
    print("Out File Prefix : " + fprefix)
    print("Temp XML file   : " + tmp_xml_file)
    print("Temp OUT file   : " + tmp_out_file)
    print("Out GCS Prefix   : " + out_transform_prefix)

    # s3 = boto3.resource('s3')
    storage_client = storage.Client()
    bucket_obj = storage_client.bucket(bucket)

    try:
        # storage_client.download_blob_to_file(bucket, key)
        blob = bucket_obj.blob(key)
        blob.download_to_filename(tmp_xml_file)
        # s3.Bucket(bucket).download_file(key, tmp_xml_file)
    except Exception as e:
        print(e)
        raise e

    ET.register_namespace("", "http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec")

    tree = ET.parse(tmp_xml_file)
    xml_data = tree.getroot()
    xmlstr = ET.tostring(xml_data, encoding='utf8', method='xml')
    xml = dict(xmltodict.parse(xmlstr))

    x = GPPXmlFlat(xml.get('measCollecFile'))
    records = x.convert_to_flat_records('gs://' + bucket + '/' + key,
                                   datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                                   'gs://' + bucket + '/' + out_transform_prefix + '/' + tmp_out_fname
                                   )

    message = 'GCS Object : gs://' + bucket + '/' + out_transform_prefix + '/' + tmp_out_fname + ' succesfully created from : s3://' + bucket + '/' + key
    # logger.info(message)
    print(message)

    if output_format == 'JSON':
        write_to_json(records, tmp_out_file)
    elif output_format == 'CSV':
        write_to_csv(x.get_record_header(), records, tmp_out_file)

    # s3.meta.client.upload_file(tmp_out_file, bucket, out_transform_prefix + '/' + tmp_out_fname)
    blob = bucket_obj.blob(out_transform_prefix + '/' + tmp_out_fname)
    blob.upload_from_filename(tmp_out_file)

    # publish messages to pubsub topic
    topic_name = os.environ['topic_name']
    publisher = pubsub_v1.PublisherClient()
    publish_to_pubsub(records, publisher, topic_name)

    return {
        'message': message
    }
