from datacatalogtordf.catalog import Catalog
from datacatalogtordf import URI
from datacatalogtordf.distribution import Distribution
import utilities
from concepttordf import Contact
from datacatalogtordf import Location
from datacatalogtordf import Agent 

IANAMEDIATYPES = "https://www.iana.org/assignments/media-types/media-types.xhtml"

class MapCatalogue:

    """A class for mapping to a dcat:Catalog.
    Ref: `dcat:Catalog <https://www.w3.org/TR/vocab-dcat-2/#Class:Catalog>`_.
    Attributes:
        catalogue (Catalogue): The catalogue base to add datasets from input source
    """
    _catalogue= None


    def __init__(self, catalog):
        self._catalogue = catalog

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
            dist.media_types = [utilities.getContenttype(media_url)]
        else:
            if utilities.validate_URL(identifier):
                dist.access_URL = identifier
        return dist


