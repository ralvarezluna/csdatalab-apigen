import json
import requests
import yaml

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