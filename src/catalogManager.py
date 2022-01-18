import yaml
import sys
from datacatalogtordf import Catalog
from datacatalogtordf import Agent
from datacatalogtordf import Document
from oastodcat import OASDataService

class CatalogueManager:

# #  Create catalog object
  catalog = Catalog()
  def __init__(self, catalog):
        self.catalog = catalog
  def __init__(self):
        self.catalog = Catalog()

  def createCatalogue(self,identifier,lang,tittle,publisher,homepage,description):
    self.catalog.identifier = identifier
    self.catalog.title = {lang: tittle}
    doc = Document()
    doc.identifier = homepage
    doc.title = {lang: tittle}
    self.catalog.homepage = doc._identifier
    agent = Agent(publisher)
    agent.name = {lang: identifier}
    self.catalog.publisher = agent
    self.catalog.description= {lang: description}
    self.catalog._conformsTo.append("https://www.w3.org/TR/vocab-dcat-2/")
    self.catalog._conformsTo.append("https://www.iana.org/assignments/media-types/text/turtle")

# # Create a dataservice based on an openAPI-specification
# # Add dataservices to catalog
  def addDataservice_from_openAPI(self,identifier,url):

    with open(url) as file:
      data = file.read()
      oas = yaml.safe_load(data)
      oas_spec = OASDataService(url, oas, identifier)
  #
  # Add dataservices to catalog:
    for dataservice in oas_spec.dataservices:
      self.catalog.services.append(dataservice)
  

  def generateRDFfile(self,filepath):
    
    dcat_out = self.catalog.to_rdf("turtle","utf-8",True,True,True)
    dcat_string = dcat_out.decode("utf-8")
    #print(dcat_string)
    with open(filepath, 'w') as f:
      sys.stdout = f # Change the standard output to the file we created.
      print(dcat_string)

    sys.stdout = sys.__stdout__
    
    
   

