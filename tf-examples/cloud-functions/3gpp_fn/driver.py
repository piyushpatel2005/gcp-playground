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
import argparse
from config import config
from pathlib import Path
import shutil

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def write_to_json(records, out_fname):
    with open(out_fname, 'w') as file_json:
        for rec in records:
            file_json.write(json.dumps(rec) + "\n")

    return None


def make_dirs(path):
    os.makedirs(path)


def cleanup_dirs(path):
    shutil.rmtree(path)


def write_to_csv(header, records, out_fname):
    with open(out_fname, 'w', encoding='utf8', newline='') as file_csv:
        fc = csv.DictWriter(file_csv,
                            fieldnames=header,
                            delimiter='|',
                            lineterminator='\n')
        fc.writeheader()
        fc.writerows(records)

    return None


def parse_args():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--output_format', help="Output format of the data. 'csv' or 'json'.")
    parser.add_argument('--input_path', help="Input path of the raw XML files")
    parser.add_argument('--output_path', help="Output path of the data in give 'output_format'.")
    parser.add_argument('--env', help="Environment parser is running against. 'local', 'dev', 'prod'.")
    return parser.parse_args()


def parse_file(file, output_path):
    print(f"Processing file {file}")
    file = str(file)
    ET.register_namespace("", "http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec")

    tree = ET.parse(file)
    xml_data = tree.getroot()
    xmlstr = ET.tostring(xml_data, encoding='utf8', method='xml')
    xml = dict(xmltodict.parse(xmlstr))

    x = GPPXmlFlat(xml.get('measCollecFile'))
    output_filename = file.split(".")[0]
    output_filename = str(Path.joinpath(output_path,  os.path.basename(file)).with_suffix(".json"))
    records = x.convert_to_flat_records(file,
                                   datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                                   str(Path.joinpath(output_path,  os.path.basename(file)).with_suffix(".json"))
                                   )
    # records = x.convert_to_records('s3://' + bucket + '/' + key,
    #                                datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
    #                                's3://' + bucket + '/' + out_transform_prefix + '/' + tmp_out_fname
    #                                )
    # print(records)
    write_to_json(records, output_filename)

def main():
    from pathlib import Path
    args = parse_args()
    # output_path = Path.cwd().joinpath("demo").joinpath("output").joinpath("csv")
    
    conf = config[args.env]
    output_path = conf.output_path
    print('Output path: ', output_path)
    if os.path.exists(output_path):
        cleanup_dirs(output_path)
    os.makedirs(output_path)
    with os.scandir(conf.input_path) as entries:
        for entry in entries:
            file_name = Path.joinpath(conf.input_path, entry.name)
            parse_file(file_name, conf.output_path)
    # parse_file(Path.joinpath(conf.input_path).joinpath('a2.xml'), conf.output_path)
    # cleanup_dirs(output_path)

if __name__ == '__main__':
    main()