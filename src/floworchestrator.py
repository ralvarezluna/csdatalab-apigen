from mapScistarterCatalogue import MapScistarter
import utilities
import mapCatalogue
import catalogManager
import generateAPIfromfile

#Load catalog configuration from properties file
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

data = None
#1) Retrieve JSON from file or remote API request
projects = []
if(source == "file"):
    data= utilities.load_json_from_file(json_file)
else:
    data= utilities.retrieve_json_from_API(api_address,api_token,"")

for i in data:
    projects.append(i)
print("Step one is finished, JSON data is loaded")

#2) Map/Parse the JSON file to DCAT Catalogue
catalogue = catalogManager.CatalogueManager()
catalogue.createCatalogue(id,lang,title,publisher,homepage,description)
scitarterMap = MapScistarter(catalogue.catalog)
catalogue.catalog = scitarterMap.parseMetadata(projects)

#3,4)Generate API and publish local
#generateAPIfromfile.generateAPI("street_story.csv", "CSV")

#5)Generate and ADD dataservice from OpenAPI spec
dcat_out = catalogue.addDataservice_from_openAPI("street_story","openapi_test.yaml")


# Persist catalog as RDF
catalogue.generateRDFfile('catalogue_output.ttl')
print("Step two is finished, the catalogue is builded from JSON metadata and RDF file was generated")


