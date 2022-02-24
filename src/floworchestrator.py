from mapscistarter import MapScistarter
import utilities
import json
import catalogmanager

#Load catalog configuration from properties file
config = utilities.load_properties("tests/config.properties")
id= config.get("cat_identifier", "http://example.com/catalogs/1")
lang = config.get("lang", "en")
title = config.get("tittle","A dataset catalog")
homepage = config.get("homepage", None)
publisher = config.get("publisher", None)
description = config.get("description", None)
source = config.get("source", "file")
json_file = config.get("file_path", None)
api_address = config.get("PLATFORM_API_URL", None)
api_token = config.get("ACCESS_TOKEN", None)

data = []
#1) Retrieve JSON from file or remote API request
projects = []
if(source == "file"):
    data= utilities.load_json_from_file(json_file)
    for i in data["entities"]:
        projects.append(i)
else:
    data = utilities.retrieve_json_from_API(api_address,api_token,"Agriculture")
    print("Retrieved")
    for i in data['entities']:
        i["_metadata"]=""
        projects.append(i)

# writing projects from the API response to file
with open('input_projects.json', 'w') as fout:
    json.dump(data, fout)


print("Step one is finished, JSON data is loaded")

#2) Map/Parse the JSON file to DCAT Catalogue
catalogue = catalogmanager.CatalogueManager()
catalogue.createCatalogue(id,lang,title,publisher,homepage,description)
scitarterMap = MapScistarter(catalogue.catalog)
catalogue.catalog = scitarterMap.parseMetadata(projects)

# Persist catalog as RDF
catalogue.generateRDFfile('catalogue_output.ttl')
print("Step two is finished, the catalogue is builded from JSON metadata and RDF file was generated")


