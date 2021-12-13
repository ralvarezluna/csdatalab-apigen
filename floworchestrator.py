import subprocess
import sys
import openAPItoDCAT
import loadProperties

## Configure csv source and project properties
csvfile = input("Enter csv file name: ")
props_file = input("Enter properties file name: ")

##Calling API generator
subprocess.call(['java', '-jar', 'ag.jar', 'csv2api', csvfile])

#Load project configuration from properties file
config = loadProperties.load_properties(props_file)
id= config.get("cat_identifier", "http://example.com/catalogs/1")
lang = config.get("lang", "en")
title = config.get("tittle","A dataset catalog")
publisher = config.get("publisher","https://example.com/publishers/1")
file_api_esp = config.get("API_spec_file", "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/examples/v3.0/petstore.yaml")

#Generate and save DCAT from OpenAPI spec
dcat_out = openAPItoDCAT.getDCAT_from_openAPI(id,lang,title,publisher,file_api_esp)
dcat_string = dcat_out.decode("utf-8")
with open('dcat_output.rdf', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    print(dcat_string)

#Update metadata to API data plattform


#Generate docker file to be ready to publish the API??

