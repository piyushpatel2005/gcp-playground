import apache_beam as beam
from main import JsonData, parse_json

def print_row(row):
    print (row)

with beam.Pipeline() as p:
    input_collection = (
        p
        | beam.io.ReadFromText("../3gpp_fn/raw/json/a1.json")
        | beam.Map(parse_json).with_output_types(JsonData)
        | beam.Map(print_row)
    )