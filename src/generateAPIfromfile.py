import subprocess
import json
import requests
import yaml
import os.path

## Configure file source and project properties

def generateAPI(file):
    """Generating API from specified file, format must be CSV"""    
    ##Calling API generator
    subprocess.call(['java', '-jar', 'ag.jar', 'csv2api', file])
    
#Parse swagger 2.0 to OpenAPI Spec 3.0.x json format
CONVERTER = "https://converter.swagger.io/api/convert"

def convertSwaggerToOpenAPI(id_file):
    swagger_path = os.path.join("AG_"+ str(id_file), "apiCode","swagger.json")
    headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
    f = open(swagger_path)
    data=json.load(f)
    r = requests.post(CONVERTER, json=data, headers=headers)
    data = r.json()

    ##Convirtiendo el json obtenido del request a Open API Spec yaml
    ff = open(id_file+".yaml", 'w+')
    yaml.dump(data, ff, allow_unicode=True)
    ff.close()    