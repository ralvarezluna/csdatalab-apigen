import sys
from concepttordf.collection import Collection
from concepttordf.definition import Definition
from datacatalogtordf import Dataset
from datacatalogtordf.catalog import Catalog
from datacatalogtordf import URI
from datacatalogtordf.distribution import Distribution
from datacatalogtordf.periodoftime import Date
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
            record.keyword = {'en': i["search_terms"]}
            collection = Collection()
            collection.identifier = "http://example.com/collections/1"
            collection.name = {"en": "A concept collection"}
            collection.name = {"nb": "En begrepssamling"}
            collection.publisher = "https://example.com/publishers/1"

            # Create a concept:
            c = Concept()
            c.identifier = "http://example.com/concepts/1"
            c.term = {"name": {"nb": "inntekt", "en": "income"}}
            definition = Definition()
            definition.text = {"nb": "ting man skulle hatt mer av",
                   "en": "something you want more of"}
            c.definition = definition

            # Add concept to collection:
            collection.members.append(c)
    
            record.theme = "https://www.wikidata.org/wiki/Q170584"
            record.landing_page = [i["signup_url"]]
            record.language = [lang]  # http://id.loc.gov/vocabulary/iso639-1/en
           
            agent = Agent(i["url"])
            agent.name = {lang: i["presenter"]}
            record.publisher = agent 
            #record.was_generated_by = {"en": i["url"]} 
            contact = Contact()
            contact._identifier= i["twitter_name"]
            contact.url= i["url"]
            record.contactpoint = contact
            location= Location(i["signup_url"])
            location.centroid= {'point': i["point"]}
            location.bounding_box = {"geographic_scope": i["geographic_scope"]["label"]}
            record.spatial_coverage = location
            record.license = i["data_license"]
            dist = Distribution(i["data_publication_url"])
            record.distributions.append(dist)
            catalog.datasets.append(record)
            
        except Exception as e:
            print(e, file=sys.stderr)
    
    return catalog

