import random
import json
import time
import utilities
import catalogManager,readCatalogueJSON

config = utilities.load_properties("config.properties")
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
for i in range(1):
    t= random.choice(topics).strip()
    source_json = utilities.retrieve_json_from_API("https://scistarter.org/p/finder?format=json&key=",
    "5-cswhNNXuutNWxx8YADcWDDbDsOslNpniUPSbMWQJ7NEr_IHRjToNVOZhLmcLUqGB--L5-OzT62qB-OxJicxA",t)
    print("Retrieved " )
    for i in source_json['entities']:
        i["_metadata"]=""
        data.append(i)


with open('tests/outputfile.json', 'w') as fout:
    json.dump(data, fout)

#2) Parse the JSON file to DCAT Catalogue
start = time.time()
catalogue = catalogManager.CatalogueManager()
catalogue.createCatalogue(id,lang,title,publisher,homepage,description)
catalogue.catalog = readCatalogueJSON.parseMetadata(data,catalogue.catalog,lang)

# Persist catalog as RDF
catalogue.generateRDFfile('catalogue_output.rdf')
print("Step two is finished, the catalogue is builded from JSON metadata and RDF file was generated")
end = time.time()
print("The time of execution of above program is :", end-start)
