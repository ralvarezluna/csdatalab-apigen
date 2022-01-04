import sys
from datacatalogtordf import Dataset
from datacatalogtordf.catalog import Catalog
from datacatalogtordf import URI
from datacatalogtordf.periodoftime import Date
import src.utilities as utilities
from concepttordf import Contact
from datacatalogtordf import Location 


def parseMetadata(source_json, catalog: Catalog, lang):
    """Mapping the JSON objects attributes to terms of data catalogue"""
    for i in source_json['entities']:
        record = Dataset()
        try:
            record.identifier =  URI(catalog.homepage + i["link"])
            record.type_genre = URI("https://dbpedia.org/ontology/Project")
            record.release_date = utilities.convertLongDate(int(i["created"]))
            record.modification_date =  utilities.convertLongDate(int(i["updated"]))
            record.title = {lang: i["name"]}
            record.description = {lang: i["description"],'goal': i["goal"], 'tasks': i["task"]}
            record.keyword = {'en': i["search_terms"]}
            record.theme = ['https://apps.usgs.gov/thesaurus/term-simple.php?thcode=2&code=2029'] #i["fields_of_science"]
            record.landing_page = [i["signup_url"]]
            record.language = [lang]  # http://id.loc.gov/vocabulary/iso639-1/en
            record.publisher = URI(i["url"])
            #record.was_generated_by = {"en": i["url"]} 
            contact = Contact()
            contact._identifier= i["twitter_name"]
            contact.url= i["url"]
            record.contactpoint = contact
            location= Location(i["signup_url"])
            location.centroid= {'point': i["point"]}
            location.bounding_box = {"geographic_scope": i["geographic_scope"]["label"]}
            record.spatial_coverage = location
            #record.distributions.
            catalog.datasets.append(record)
        except Exception as e:
            print(e, file=sys.stderr)
    
    return catalog

