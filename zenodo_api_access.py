import json
import requests

data = {
    "metadata": {
        "title": "CS_demo",
        "upload_type": "dataset",
        "description": "This is an example of CS project to share data services throug DCAT spec",
        "creators": [
            {"name": "Alvarez, Reynaldo", "affiliation": "UCI/UA"}
        ],
        "subjects":[{"term": "dcat:DataService", "identifier": "http://my_csexample.org/api/v1", "scheme": "url"}]
    }
}
url = "https://sandbox.zenodo.org/api/deposit/depositions/978307?access_token=TRG7j3vXaHDuV5eAAP0KahomFbHdvWs1CM9H39Lj7RVXCTAZrPJoTaQSkmfi"
headers = {"Content-Type": "application/json"}

r = requests.put(url, data=json.dumps(data), headers=headers)

