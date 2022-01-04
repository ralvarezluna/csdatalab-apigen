import sys

from datacatalogtordf.catalog import Catalog
import src.utilities as utilities
import src.readCatalogueJSON as readCatalogueJSON
import src.catalogManager as catalogManager

#Load catalog configuration from properties file
config = utilities.load_properties("config.properties")
id= config.get("cat_identifier", "http://example.com/catalogs/1")
lang = config.get("lang", "en")
title = config.get("tittle","A dataset catalog")
publisher = config.get("homepage", None)
file_api_esp = config.get("api_spec_file", None)
source = config.get("source", "file")
json_file = config.get("file_path", None)
api_address = config.get("PLATFORM_API_URL", None)
api_token = config.get("ACCESS_TOKEN", None)


#1) Retrieve JSON from file or remote API request
if(source == "file"):
    data= utilities.load_json_from_file(json_file)
else:
    data= utilities.retrieve_json_from_API(api_address,api_token)

print("Step one is finished, JSON data is loaded")

#2) Parse the JSON file to DCAT Catalogue
catalogue = catalogManager.CatalogueManager()
catalogue.createCatalogue(id,lang,title,publisher)
catalogue.catalog = readCatalogueJSON.parseMetadata(data,catalogue.catalog,lang)

# Persist catalog as RDF
catalogue.generateRDFfile('catalogue_output.rdf')
print("Step two is finished, the catalogue is builded from JSON metadata and RDF file was generated")

#Generate and save DCAT from OpenAPI spec
#dcat_out = catalogManager.getDCAT_from_openAPI(file_api_esp)


#Update metadata to API data plattform


