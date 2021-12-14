from subprocess import TimeoutExpired
import yaml
import requests
from datacatalogtordf import Catalog
from oastodcat import OASDataService

# # Create catalog object
# catalog = Catalog()
# catalog.identifier = "http://example.com/catalogs/1"
# catalog.title = {"en": "A dataset catalog"}
# catalog.publisher = "https://example.com/publishers/1"

# # Create a dataservice based on an openAPI-specification:
# url = ("https://raw.githubusercontent.com/"
#       "OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml"
#      )
# oas = yaml.safe_load(requests.get(url).text)
# identifier = "http://example.com/dataservices/{id}"
# oas_spec = OASDataService(url, oas, identifier)
# #
# # Add dataservices to catalog:
# for dataservice in oas_spec.dataservices:
#   catalog.services.append(dataservice)

# #get dcat representation in turtle (default)
# dcat = catalog.to_rdf()

# print(dcat)

def getDCAT_from_openAPI(identifier,lang,tittle,publisher,file_url):

  catalog = Catalog()
  catalog.identifier = identifier
  catalog.title = {lang: tittle}
  catalog.publisher = publisher  
  url = file_url
  with open(url) as file:
    data = file.read()
  oas = yaml.safe_load(data)
  oas_spec = OASDataService(url, oas, identifier)
  #
  # Add dataservices to catalog:
  for dataservice in oas_spec.dataservices:
    catalog.services.append(dataservice)
  
  dcat = catalog.to_rdf()

  return dcat
