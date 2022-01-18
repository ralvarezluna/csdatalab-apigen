import sys

from datacatalogtordf import Dataset
from datacatalogtordf.catalog import Catalog
from datacatalogtordf import URI
from datacatalogtordf.distribution import Distribution
from datacatalogtordf.document import Document
import utilities
from concepttordf import Contact
from location import ownLocation
from datacatalogtordf import Agent 

def parseMetadata(source_json:list, catalog: Catalog, lang) -> Catalog:
    """Mapping the JSON objects attributes to terms of data catalogue"""
    print("Processing " + len(source_json).__str__() + " projects" )
    x=0
    sdgs = utilities.load_properties("sdgs_semantic.properties")
    for i in source_json:
        record = Dataset()
        try:
            record.identifier =  URI(catalog.homepage + i["link"])
            record.type_genre = URI("https://dbpedia.org/ontology/Project")  #
            record.release_date = utilities.convertLongDate(int(i["created"]))
            record.modification_date =  utilities.convertLongDate(int(i["updated"]))
            record.title = {lang: i["name"]}
            record.description = {lang: i["description"]+ " GOAL " + i["goal"] + " TASKS " + i["task"]}
            record.keyword = {lang: i["search_terms"]}
                        
            #Anotate as themes the relation with SDGs
            themes = []
            themes.append(URI("https://www.wikidata.org/wiki/Q170584"))
            ref_goals = utilities.extractNumbers(i["sustainable_development_goals"])
            for j in ref_goals:
                themes.append(URI(sdgs.get(j,None)))
            record.theme = themes
            
            record._conformsTo.append("https://www.w3.org/TR/vocab-dcat-2/")

            record.landing_page = {i["url"]} 
            print(i["url"])
            #if utilities.validate_URL(i["signup_url"]):
            #    record.landing_page = [i["signup_url"]]
            #else:
            #    if utilities.validate_URL(i["url"]):
            #        record.landing_page = i["url"]  
            #    else:
            #        record.landing_page = catalog.homepage + i["link"]
                       
            record.language = [lang]  # http://id.loc.gov/vocabulary/iso639-1/en
           
            agent = Agent(i["url"])
            agent.name = {lang: i["presenter"]}
            record.publisher = agent 
            #record.was_generated_by = {"en": i["url"]} 
            
            contact = Contact()
            contact.name = {lang: i["presenter"]}
            contact.email = "example@ex.com"
            contact._identifier= {lang: i["twitter_name"]}
            contact.url = i["url"]
            record.contactpoint = contact

            #record.license = {lang: i["data_license"]}

            loc = ownLocation()
            loc.geometry = i["regions"]
            loc.identifier = record.identifier
            loc.centroid= {'point': i["point"]}
            loc.bounding_box = {"geographic_scope": i["geographic_scope"]["label"]}
            record.spatial_coverage = loc
            
            if utilities.validate_URL(i["data_license"]):
                uri = URI(i["data_license"])
                record.license = uri

            dist = Distribution(i["url"])
            if utilities.validate_URL(i["data_publication_url"]):
                dist.access_URL = i["data_publication_url"]
                record.distributions.append(dist)
            else:
                if utilities.validate_URL(i["url"]):
                    dist.access_URL = i["url"]
                    record.distributions.append(dist)
            catalog.datasets.append(record)
            x += 1
        except Exception as e:
            print(e, file=sys.stderr)
            print("The project " + i["guid"] + " not parsed due to problems with metadata")
    print("Was parsed an amount of " + str(x) + " projects" )
    return catalog

