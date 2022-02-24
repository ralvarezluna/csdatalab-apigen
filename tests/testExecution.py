import random
import json
import time
from src.mapscistarter import MapScistarter
from catalogmanager import CatalogueManager
from src.utilities import utilities


config = None
config = utilities.load_properties("tests/config.properties")
id= config.get("cat_identifier", "http://example.com/catalogs/1")
lang = config.get("lang", "en")
title = config.get("tittle","A dataset catalog")
homepage = config.get("homepage", None)
publisher = config.get("publisher", None)
description = config.get("description", None)
file_api_esp = config.get("api_spec_file", None)
source = config.get("source", "file")
json_file = config.get("file_path", None)
api_address = config.get("PLATFORM_API_URL", None)
api_token = config.get("ACCESS_TOKEN", None)

with open("tests/topics.txt", "r") as file:
    topics = file.readlines()
    
    
source_json = []
data = []
for i in range(3):
    t= random.choice(topics).strip()
    source_json = ut.retrieve_json_from_API(api_address, api_token,t)
    print("Retrieved")
    for i in source_json['entities']:
        i["_metadata"]=""
        data.append(i)


with open('tests/outputfile.json', 'w') as fout:
    json.dump(data, fout)

#2) Parse the JSON file to DCAT Catalogue
start = time.time()
catalogue = catalogmanager.CatalogueManager()
catalogue.createCatalogue(id,lang,title,publisher,homepage,description)
scitarterMap = MapScistarter(catalogue.catalog)
catalogue.catalog = scitarterMap.parseMetadata(data)

# Persist catalog serialized as Turtle
catalogue.generateRDFfile('tests/catalogue_output.ttl')
print("Step two is finished, the catalogue is builded from JSON metadata and RDF file was generated")
end = time.time()
print("The time of execution of above program is :", end-start)
