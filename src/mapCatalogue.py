import sys
from datacatalogtordf.catalog import Catalog
from datacatalogtordf import URI
from datacatalogtordf.distribution import Distribution
from src import utilities
from src.generateapifromfile import *
from concepttordf import Contact
from datacatalogtordf import Location
from datacatalogtordf import Agent 
from oastodcat import OASDataService
import yaml

IANAMEDIATYPES = "https://www.iana.org/assignments/media-types/"
class MapCatalogue:

    """A class for mapping to a dcat:Catalog.
    Ref: `dcat:Catalog <https://www.w3.org/TR/vocab-dcat-2/#Class:Catalog>`_.
    Attributes:
        catalogue (Catalogue): The catalogue base to add datasets and dataservices from input source
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

    def  createDistribution(self,identifier, media_url, id)->Distribution:
        '''Creates a distribution for the identifier Dataset 
        refering the data access url
        The field id wild be used to creates Web API folder'''
        dist = Distribution(identifier)
        if utilities.validate_URL(media_url):
            dist.access_URL = media_url
            media_type = utilities.getContenttype(media_url,str(id))
            media_type = media_type.split(";")[0]
            dist.media_types = [IANAMEDIATYPES+media_type]
            if(media_type=="text/csv" or media_type=="application/json"):
                self.addDataServices(identifier,id)
        else:
            if utilities.validate_URL(identifier):
                dist.access_URL = identifier
        return dist
    
    def addDataServices(self,identifier,id)->None:
        '''Add dataservice specification to DCAT catalogue after the generation of Web APIs packages
            identifier: id of dataservice
            id: project id to identify Web APIs throug the project ID        
        '''
        try:
            generateAPI(str(id)+".csv")
        except  Exception as e:
            print(e, file=sys.stderr)
            print("The API from resource " + identifier + " can´t be generated, check process or source")
            return
        
        convertSwaggerToOpenAPI(str(id))
        #Reading OpenAPI Specification from file
        
        with open(str(id)+'.yaml') as f:
            oas = yaml.safe_load(f)
        oas_spec = OASDataService(identifier, oas, identifier)
        # Add dataservices to catalog:
        for dataservice in oas_spec.dataservices:
            self._catalogue.services.append(dataservice)
        

