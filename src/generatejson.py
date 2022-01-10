import json
import random

from requests.models import Response
import utilities

with open("tests/topics.txt", "r") as file:
    topics = file.readlines()
    
    
source_json = []
data = []
for i in range(2):
    t= random.choice(topics).strip()
    source_json = utilities.retrieve_json_from_API("https://scistarter.org/p/finder?format=json&key=",
    "5-cswhNNXuutNWxx8YADcWDDbDsOslNpniUPSbMWQJ7NEr_IHRjToNVOZhLmcLUqGB--L5-OzT62qB-OxJicxA",t)
    for i in source_json['entities']:
        data.append(i)

#result =[]
#for entities in source_json:
#    result.append(source_json['entities'])
print(data.__sizeof__()) 
