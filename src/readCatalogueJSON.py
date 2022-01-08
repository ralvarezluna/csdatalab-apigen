import re
import sys
from concepttordf.collection import Collection
from concepttordf.contact import VCARD
from concepttordf.definition import Definition
from datacatalogtordf import Dataset
from datacatalogtordf.catalog import Catalog
from datacatalogtordf import URI
from datacatalogtordf.distribution import Distribution
from datacatalogtordf.periodoftime import Date
from datacatalogtordf.relationship import Relationship
from datacatalogtordf.resource import Resource
import src.utilities as utilities
from concepttordf import Contact
from concepttordf import Concept
from datacatalogtordf import Location 
from datacatalogtordf import Agent 

def parseMetadata(source_json, catalog: Catalog, lang):
    """Mapping the JSON objects attributes to terms of data catalogue"""
    for i in source_json['entities']:
        record = Dataset()
        try:
            record.identifier =  URI(catalog.homepage + i["link"])
            record.type_genre = URI("https://dbpedia.org/ontology/Project")  #
            record.release_date = utilities.convertLongDate(int(i["created"]))
            record.modification_date =  utilities.convertLongDate(int(i["updated"]))
            record.title = {lang: i["name"]}
            record.description = {lang: i["description"]+ " GOAL " + i["goal"] + " TASKS " + i["task"]}
            record.keyword = {lang: i["search_terms"]}
                        
            #Anotate as themes the relation with SDG
            sdgs = utilities.load_properties("sdgs_semantic.properties")
            themes = []
            themes.append(URI("https://www.wikidata.org/wiki/Q170584"))
            ref_goals = utilities.extractNumbers(i["sustainable_development_goals"])
            for j in ref_goals:
                themes.append(URI(sdgs.get(j,None)))
            record.theme = themes
            
            record.landing_page = [i["signup_url"]]
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

            record.license = {lang: i["data_license"]}

            location = Location(i["signup_url"])
            location.identifier = "IDENTIFIER"
            location.centroid= {'point': i["point"]}
            location.bounding_box = {"geographic_scope": i["geographic_scope"]["label"]}
            record.spatial_coverage = location
            record.license = i["data_license"]
            dist = Distribution(i["url"])
            if(i["data_publication_url"] == ""):
                dist.access_URL = i["url"]
            else:
                dist.access_URL = i["data_publication_url"]
            record.distributions.append(dist)
            catalog.datasets.append(record)
        except Exception as e:
            print(e, file=sys.stderr)
    
    return catalog

