
import sys
from typing import Optional
from datacatalogtordf import Dataset
from datacatalogtordf.catalog import Catalog
from datacatalogtordf import URI
from mapCatalogue import MapCatalogue
import utilities


IANAMEDIATYPES = "https://www.iana.org/assignments/media-types/media-types.xhtml"

class MapScistarter(MapCatalogue):

    def __init__(self, catalogue) -> None:
        """Inits catalog object with default values."""
        super().__init__(catalogue)


    def parseMetadata(self,source_json:list) -> Catalog:
        """Mapping the JSON objects attributes to terms of Scistarter data catalogue"""
        print("Processing " + len(source_json).__str__() + " projects" )
        x=0 
        lang = "en"
        sdgs = utilities.load_properties("sdgs_semantic.properties")
        for i in source_json:
            record = Dataset()
            try:
                record.identifier =  URI(self._catalogue.homepage + i["link"])
                record.type_genre = URI("https://dbpedia.org/ontology/Project")  #
                record.release_date = utilities.convertLongDate(int(i["created"]))
                record.modification_date =  utilities.convertLongDate(int(i["updated"]))
                record.title = {lang: i["name"]}
                record.description = {lang: i["description"]+ " GOAL " + i["goal"] + " TASKS " + i["task"]}
                record.keyword = {lang: i["search_terms"]}
            #record.access_rights_comments.append(i["data_access"])   
            
                #Anotate as themes the relation with SDGs
                themes = []
                themes.append(URI("https://www.wikidata.org/wiki/Q170584"))
                ref_goals = utilities.extractNumbers(i["sustainable_development_goals"])
                for j in ref_goals:
                    themes.append(URI(sdgs.get(j,None)))
                    record.theme = themes
            
                record._conformsTo.append("https://www.w3.org/TR/vocab-dcat-2/")

                if i["url"]:
                    record.landing_page.append(i["url"]) 
                    print(i["url"])
                #Defining dataset language, by default inherits catalogue language                       
                record.language = [lang]  # http://id.loc.gov/vocabulary/iso639-1/en
           
                #Mapping the agent of the resource
                record.publisher = self.createAgent(i["url"],lang,{lang: i["presenter"]})

                #Mapping contact point details
                record.contactpoint = self.createContact({lang: i["presenter"]},{lang: i["twitter_name"]}
                ,i["participation_notification_email"],i["url"],lang)

                #Mapping location
                record.spatial_coverage = self.createLocation(record.identifier, i["regions"],
                {'point': i["point"]},i["geographic_scope"]["label"])

                #Specifying data license
                license = self.addLicense(i["data_license"])
                if license:
                    record.license = license

                #Defining a Distribution for the data referenced in the input
                dist = self.createDistribution(i["url"],i["data_publication_url"])

                #Add referenced distribution, if the input have more than one, you must repeat the procedure
                record.distributions.append(dist)

                #Adding the mapped record to the catalogue
                self._catalogue.datasets.append(record)
                x += 1
            except Exception as e:
                print(e, file=sys.stderr)
                print("The project " + i["link"] + " not parsed due to problems with metadata")
        print("Was parsed an amount of " + str(x) + " projects" )
        return self._catalogue
