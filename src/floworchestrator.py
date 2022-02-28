import string
from src import catalogmanager, utilities
from src.mapscistarter import MapScistarter
import json
class MainController():
   
    _config = dict
    _id_catalogue = None
    _catalogue = None

    def __init__(self,config_path:string):
        #Load catalog configuration from properties file
        self._config = utilities.load_properties(config_path)
        self._id_catalogue = self._config.get("cat_identifier", "http://example.com/catalogs/1")
        self._catalogue = catalogmanager.CatalogueManager()
    

    def readDatafromSource(self,query:string) -> list:
        source = self._config.get("source", "file")
        json_file = self._config.get("file_path", None)
        api_address = self._config.get("PLATFORM_API_URL", None)
        api_token = self._config.get("ACCESS_TOKEN", None)
        data = []
        #1) Retrieve JSON from file or remote API request
        projects = []
        if(source == "file"):
            data= utilities.load_json_from_file(json_file)
            for i in data["entities"]:
                projects.append(i)
        else:
            data = utilities.retrieve_json_from_API(api_address,api_token,query)
        print("Retrieved projects from JSON source")
        for i in data['entities']:
            i["_metadata"]=""
            projects.append(i)

        # writing projects from the API response to file
        with open('input_projects.json', 'w') as fout:
            json.dump(data, fout)
        print("Metadata gathered is saved in the file input_projects.json in the root directory")
        print("Step one is finished, JSON data is loaded")
        return projects

    #2) Map/Parse the JSON file to DCAT Catalogue, during the process Web APIs 
    # will be generated for available datasets
    def mapMetadata(self,projects:list):
        id= self._config.get("cat_identifier", "http://example.com/catalogs/1")
        lang = self._config.get("lang", "en")
        title = self._config.get("tittle","A dataset catalog")
        homepage = self._config.get("homepage", None)
        publisher = self._config.get("publisher", None)
        description = self._config.get("description", None)

        self._catalogue.createCatalogue(id,lang,title,publisher,homepage,description)
        scitarterMap = MapScistarter(self._catalogue.catalog)
        self._catalogue.catalog = scitarterMap.parseMetadata(projects)
        print("Metadata was parsed to DCAT")

    # Persist catalog as RDF
    def generateRDFoutput(self,output_path:string):
        self._catalogue.generateRDFfile('catalogue_output.ttl')
        print("DCAT resource generation is finished, the catalogue is builded from JSON metadata and RDF file was generated")


