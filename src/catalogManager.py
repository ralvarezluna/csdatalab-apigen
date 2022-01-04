from subprocess import TimeoutExpired
import yaml
import sys
from datacatalogtordf import Catalog
from oastodcat import OASDataService

class CatalogueManager:

# #  Create catalog object
  catalog = Catalog()
  def __init__(self, catalog):
        self.catalog = catalog
  def __init__(self):
        self.catalog = Catalog()
# print(dcat)
  def createCatalogue(self,identifier,lang,tittle,publisher):
    self.catalog.identifier = identifier
    self.catalog.title = {lang: tittle}
    self.catalog.homepage = publisher 

# # Create a dataservice based on an openAPI-specification
# # Add dataservices to catalog
  def getDCAT_from_openAPI(self,identifier,lang,tittle,publisher,file_url):

    
    url = file_url
    with open(url) as file:
      data = file.read()
      oas = yaml.safe_load(data)
      oas_spec = OASDataService(url, oas, identifier)
  #
  # Add dataservices to catalog:
    for dataservice in oas_spec.dataservices:
      self.catalog.services.append(dataservice)
  
    dcat = self.catalog.to_rdf()
  
    return dcat

  def generateRDFfile(self,filepath):
    dcat_out = self.catalog.to_rdf("turtle","utf-8",True,True,True)
    dcat_string = dcat_out.decode("utf-8")
    print(dcat_string)
    with open(filepath, 'w') as f:
      sys.stdout = f # Change the standard output to the file we created.
      print(dcat_string)
   

