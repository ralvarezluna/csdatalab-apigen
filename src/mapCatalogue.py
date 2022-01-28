import sys
from datacatalogtordf.catalog import Catalog
from datacatalogtordf import URI
from datacatalogtordf.distribution import Distribution
from generateAPIfromfile import generateAPI
import utilities
from concepttordf import Contact
from datacatalogtordf import Location
from datacatalogtordf import Agent 
from oastodcat import OASDataService
import yaml

IANAMEDIATYPES = "https://www.iana.org/assignments/media-types/media-types.xhtml"

class MapCatalogue:

    """A class for mapping to a dcat:Catalog.
    Ref: `dcat:Catalog <https://www.w3.org/TR/vocab-dcat-2/#Class:Catalog>`_.
    Attributes:
        catalogue (Catalogue): The catalogue base to add datasets from input source
    """
    _catalogue= Catalog()


    def __init__(self, catalogue:Catalog):
        self._catalogue = catalogue

    def parseMetadata(self,source_json:list) -> Catalog:
        '''Define this method for mapping the specific source'''
        pass

    def createAgent(self,url, lang, presenter)->Agent:
        '''Creating agent, agent represents a FOAF agent, the publisher of the resource'''
        agent = Agent(url)
        agent.name = {lang: presenter}
        return agent

    def createContact(self,name,identifier,email,url,lang)->Contact:
        '''Details of contact to the shared resource'''
        contact = Contact()
        contact.name = {lang: name}
        contact.email = email
        contact._identifier= {lang: identifier}
        contact.url = url
        return contact

    def createLocation(self,identifier,regions, center_point,geographic_scope)->Location:
        '''Create location for the dataset recognised with identifier, specifying regions,
        center_point and geographic scope'''
        loc = Location()
        loc.geometry = regions
        loc.identifier = identifier
        loc.centroid= {'point': center_point}
        loc.bounding_box = {"geographic_scope": geographic_scope}
        return loc

    def addLicense(self,license)->URI:
        '''Validate if the license is defined in the input as a valid URI type,
        returns a URI object is the input license is valid '''
        if utilities.validate_URL(license):
            uri = URI(license)
            return uri
        return None

    def  createDistribution(self,identifier, media_url)->Distribution:
        '''Creates a distribution for the identifier Dataset 
        refering the data access url'''
        dist = Distribution(identifier)
        if utilities.validate_URL(media_url):
            dist.access_URL = media_url
            media_type = utilities.getContenttype(media_url,"aa.csv")
            dist.media_types = [media_type]
            self.addDataServices(media_type,identifier)
        else:
            if utilities.validate_URL(identifier):
                dist.access_URL = identifier
        return dist
    
    def addDataServices(self,media_type,identifier)->None:
        if(media_type == "text/csv"):
            try:
                generateAPI("aa.csv",'CSV')
            except  Exception as e:
                print(e, file=sys.stderr)
                print("The API from resource " + identifier + " can´t be generated, check process or source")
                return
        oas = yaml.safe_load(self.minimal_spec())
        oas_spec = OASDataService('localhost:8080', oas, identifier)
        # Add dataservices to catalog:
        for dataservice in oas_spec.dataservices:
            self._catalogue.services.append(dataservice)
        

    def minimal_spec(self) -> str:
        """Helper for creating a minimal specification object."""
        _minimal_spec = """
                    openapi: 3.0.3
                    info:
                      title: Swagger Petstore
                      version: 1.0.0
                    paths: {}
                    """
        return _minimal_spec
        

