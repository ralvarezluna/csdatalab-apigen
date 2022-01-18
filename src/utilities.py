import validators
import json
import re
from datacatalogtordf.periodoftime import Date
import requests
import sys
import time

from requests.models import Response

def load_properties(filepath):
    sep=':'
    comment_char='#'
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"') 
                props[key] = value 
    return props

def load_json_from_file(filepath):
    try:
        with open(filepath) as f:
            data = json.load(f)   
    except FileNotFoundError as e:
         print(e, file=sys.stderr)
    return data

def retrieve_json_from_API(remote_address, token, query): 
    q = "&q=" + query
    try:
        response = requests.get(remote_address+token+q)
    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
    return response.json()

def convertLongDate(long_date):
    date_format = '%m/%d/%Y'
    struct = time.gmtime(long_date/1000.)
    dt = time.strftime('%Y-%m-%d', struct)
    return dt

def extractNumbers(joined_sdgs: str):
    return re.findall(r'\d+', joined_sdgs)
    

def validate_URL(url) ->bool:
    if not url:
        return False
    if validators.url(url):
        return True
    return False        


