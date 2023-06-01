import apache_beam as beam
from main import JsonData, parse_json
import xml.etree.ElementTree as ET
import xmltodict
import apache_beam.io.fileio as fileio
from pathlib import Path
import os
import datetime
import json

from GPPXmlFlat import GPPXmlFlat

def cleanup(row):
    newrow = row[1].replace("\n", "")
    final = newrow.replace("\t", "")
    return (row[0], final)

def print_row(row):
    print (row)

def create_dict(row):
    ET.register_namespace("", "http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec")

    # tree = ET.parse(file)
    # xml_data = tree.getroot()
    # xmlstr = ET.tostring(xml_data, encoding='utf8', method='xml')
    tree = ET.ElementTree(ET.fromstring(row[1]))
    xml_data = tree.getroot()
    xmlstr = ET.tostring(xml_data, method='xml')
    xml = dict(xmltodict.parse(xmlstr))
    xml['file_name'] = row[0]
    return xml

class ConverToJsonDict(beam.DoFn):
#     def __init__(self, json_parser):
#         self.json_parser = json_parser

    def process(self, element):
        json_parser = GPPXmlFlat(element.get('measCollecFile'))
        records = json_parser.convert_to_flat_records(element['file_name'],
                                   datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                                   "something"
                                   )
        return records
    
def parse_json(element):
#     row = json.load(element)
    return JsonData(**element)


str = """<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="MeasDataCollection.xsl"?>
<measCollecFile xmlns="http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec"
xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
xsi:schemaLocation="http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec">
        <fileHeader fileFormatVersion="32.435 V7.0" vendorName="Company NN" dnPrefix="DC=a1.companyNN.com,SubNetwork=1,IRPAgent=1">
                <fileSender localDn="SubNetwork=CountryNN,MeContext=MEC-Gbg-1,ManagedElement=RNC-Gbg-1" elementType="RNC"/>
                <measCollec beginTime="2000-03-01T14:00:00+02:00"/>
        </fileHeader>
        <measData>
                <managedElement localDn="SubNetwork=CountryNN,MeContext=MEC-Gbg-1,ManagedElement=RNC-Gbg-1" userLabel="RNC Telecomville"/>
                <measInfo>
                        <job jobId="1231"/>
                        <granPeriod duration="PT900S" endTime="2000-03-01T14:14:30+02:00"/>
                        <repPeriod duration="PT1800S"/>
                        <measTypes>attTCHSeizures succTCHSeizures attImmediateAssignProcs succImmediateAssignProcs</measTypes>
                        <measValue measObjLdn="RncFunction=RF-1,UtranCell=Gbg-997">
                                <measResults>234 345 567 789</measResults>
                        </measValue>
                        <measValue measObjLdn="RncFunction=RF-1,UtranCell=Gbg-998">
                                <measResults>890 901 123 234</measResults>
                        </measValue>
                        <measValue measObjLdn="RncFunction=RF-1,UtranCell=Gbg-999">
                                <measResults>456 567 678 789</measResults>
                                <suspect>true</suspect>
                        </measValue>
                </measInfo>
        </measData>
        <fileFooter>
                <measCollec endTime="2000-03-01T14:15:00+02:00"/>
        </fileFooter>
</measCollecFile>"""


str2 = """<?xml version="1.0" encoding="UTF-8"?><!-- Sample PM File. All values are hypothetical but syntactically correct --><measCollecFile xmlns="http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec"><fileHeader fileFormatVersion="32.435 v6.1" vendorName="Company NN" dnPrefix="SubNetwork=1"><fileSender elementType="Element Manager" localDn="OMC_PS=10"/><measCollec beginTime="2005-06-09T13:00:00-05:00"/></fileHeader><measData><managedElement localDn="ManagedElement=PS_Core" userLabel="SGSN" swVersion="R30.1.5"/><measInfo measInfoId="Category A"><job jobId="01"/><granPeriod endTime="2005-06-09T13:15:00-06:00" duration="PT900S"/><repPeriod duration="PT1800S"/><measTypes>MM.AttGprsAttach MM.SuccGprsAttach MM.AbortedGprsAttach MM.AttIntraSgsnRaUpdate</measTypes><measValue measObjLdn="SgsnFunction=1"><measResults>10 20 30 40</measResults></measValue></measInfo><measInfo measInfoId="Category B"><job jobId="02"/><granPeriod endTime="2005-06-09T13:15:00-06:00" duration="PT900S"/><repPeriod duration="PT1800S"/><measTypes>MM.AttCombiAttach MM.SuccCombiAttach MM. MM.AbortedCombiAttachMM.AttCombiDetachMs</measTypes><measValue measObjLdn="SgsnFunction=2"><measResults>50 60 70 80</measResults></measValue></measInfo><measInfo measInfoId="Category C"><job jobId="03"/><granPeriod endTime="2005-06-09T13:15:00-06:00" duration="PT1800S"/><repPeriod duration="PT900S"/><measTypes>MM.AttPsPagingProcIu MM.SuccPsPagingProcIu</measTypes><measValue measObjLdn="SgsnFunction=3"><measResults>25 30</measResults></measValue></measInfo></measData><fileFooter><measCollec endTime="2005-06-09T13:15:00-06:00"/></fileFooter></measCollecFile>"""
ET.register_namespace("", "http://www.3gpp.org/ftp/specs/archive/32_series/32.435#measCollec")
tree = ET.ElementTree(ET.fromstring(str2))
xml_data = tree.getroot()
# print(tree)
xmlstr = ET.tostring(xml_data)
xml = dict(xmltodict.parse(xmlstr), method='xml')
# print(xml)
x = GPPXmlFlat(xml.get('measCollecFile'))
file = "something"
output_path = "another"
# output_filename = file.split(".")[0]
# output_filename = str(Path.joinpath(output_path,  os.path.basename(file)).with_suffix(".json"))
output_filename = "output_name.json"
records = x.convert_to_flat_records(file,
                                datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                                output_filename
                                )
# print(records)
with beam.Pipeline() as p:
#     input_collection = (
#         p
#         | beam.io.ReadFromText("../3gpp_fn/raw/xml/a1.xml")
#         | beam.Map(create_dict)
#         | beam.Map(print_row)
#     )

    readable_files = (
        p
        | fileio.MatchContinuously("../3gpp_fn/raw/xml2/*.xml")
        | fileio.ReadMatches()
        | beam.Reshuffle()
    )

    files_and_contents = (
        readable_files
        | beam.Map(lambda x: (x.metadata.path, x.read_utf8()))
        | beam.Map(create_dict)
        | beam.ParDo(ConverToJsonDict())
        | beam.Map(parse_json).with_output_types(JsonData)
        | beam.Map(print_row)
    )

    p.run().wait_until_finish()