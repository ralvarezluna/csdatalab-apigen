from contextlib import nullcontext
import json
import subprocess
import sys
import requests
import yaml
import pandas as pd

import loadProperties
import openAPItoDCAT

## Configure file source and project properties

props_file = input("Enter properties file name: ")
csvfile = input("Enter csv file name: ")

##Covert from JSON to CSV
if(csvfile == ''):
    jsonfile = input("Enter json file name: ")
    df = pd.read_json (jsonfile)
    df.to_csv (r'generated.csv', index = None)
    subprocess.call(['java', '-jar', 'ag.jar', 'csv2api', 'generated.csv'])
##Calling API generator
else:
    subprocess.call(['java', '-jar', 'ag.jar', 'csv2api', csvfile])

#Load project configuration from properties file
config = loadProperties.load_properties(props_file)
id= config.get("cat_identifier", "http://example.com/catalogs/1")
lang = config.get("lang", "en")
title = config.get("tittle","A dataset catalog")
publisher = config.get("publisher","https://example.com/publishers/1")
file_api_esp = config.get("API_spec_file", "openapi.yaml")

#Parse swagger 2.0 to OpenAPI Spec 3.0.x json format
url = "https://converter.swagger.io/api/convert"
headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
f = open('AG_demodata/apiCode/swagger.json')
data=json.load(f)
r = requests.post(url, json=data, headers=headers)
data = r.json()

##Convirtiendo el json obtenido del request a Open API Spec yaml
ff = open('openapi_test.yaml', 'w+')
yaml.dump(data, ff, allow_unicode=True)
ff.close()

#Generate and save DCAT from OpenAPI spec
dcat_out = openAPItoDCAT.getDCAT_from_openAPI(id,lang,title,publisher,file_api_esp)
dcat_string = dcat_out.decode("utf-8")
with open('dcat_output.rdf', 'w') as f:
    sys.stdout = f # Change the standard output to the file we created.
    print(dcat_string)

#Update metadata to API data plattform


#Generate docker file to be ready to publish the API??

