from subprocess import TimeoutExpired
import yaml
import requests
from datacatalogtordf import Catalog
from oastodcat import OASDataService

# # Create catalog object
catalog = Catalog()
catalog.identifier = "http://example.com/catalogs/1"
catalog.title = {"en": "A dataset catalog"}
catalog.publisher = "https://example.com/publishers/1"

 # Create a dataservice based on an openAPI-specification:
urlxx = ("https://raw.githubusercontent.com/"
      "OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml"
     )

url = "openapi.yaml"
with open(url) as file:
    data = file.read()
oas = yaml.safe_load(data)
identifier = "http://example.com/dataservices/{id}"
oas_spec = OASDataService(url,oas, identifier)
# #
# # Add dataservices to catalog:
for dataservice in oas_spec.dataservices:
   catalog.services.append(dataservice)
 #get dcat representation in turtle (default)
dcat = catalog.to_rdf()

print(dcat)

#curl -i -vX POST https://converter.swagger.io/api/convert   -H "Content-Type: application/json" --data-binary "@AG_demodata/apiCode/swagger.json" -o ./openapi.yaml
#curl -i -vX POST https://mermade.org.uk/openapi-converter/api/v1/convert   -H "Content-Type: application/json" --data-binary "@AG_demodata/apiCode/swagger.json" -o ./openapi.yaml

