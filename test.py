import requests
import json

url = "https://converter.swagger.io/api/convert"
headers = {"content-type": "application/json", "Accept-Charset": "UTF-8"}
f = open('AG_demodata/apiCode/swagger.json')
data=json.load(f)
r = requests.post(url, json=data, headers=headers)
data = r.json()
print(data)