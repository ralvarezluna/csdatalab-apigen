import validators
import json
import re
import requests
import sys
import time
import pandas as pd

'''Auxiliar file to define support functions, formats conversion, file management...'''

def load_properties(filepath):
    '''Support the reading of properties files, returns a properties object'''
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
    '''Load the json content from local file'''
    try:
        with open(filepath) as f:
            data = json.load(f)   
    except FileNotFoundError as e:
         print(e, file=sys.stderr)
    return data

def retrieve_json_from_API(remote_address, token, query): 
    '''Process a http request to the remote address, providing token and query'''
    q = "&q=" + query
    try:
        response = requests.get(remote_address+token+q)
    except requests.exceptions.RequestException as e:
        print(e, file=sys.stderr)
    return response.json()

def convertLongDate(long_date):
    '''Converting date in long format to %m/%d/%Y'''
    date_format = '%m/%d/%Y'
    struct = time.gmtime(long_date/1000.)
    dt = time.strftime('%Y-%m-%d', struct)
    return dt

def extractNumbers(joined_sdgs: str):
    '''Extract numbers from string'''
    if(joined_sdgs):
        return re.findall(r'\d+', joined_sdgs)
    return []
    

def validate_URL(url) ->bool:
    '''Validate the URL through python common validators'''
    if not url:
        return False
    if validators.url(url):
        return True
    return False        

def getContenttype(media_url,identifier):
    '''Check the content-type of the URL request for checking data format'''
    response = requests.head(media_url)
    r= response.headers['content-type']
    configureResponseToFile(r,media_url,identifier)
    print("El tipo de dato público es " + r)
    return r

def configureResponseToFile(resp,media_url,identifier):
    response = requests.get(media_url, stream=True)
    # Throw an error for bad status codes
    response.raise_for_status()

    if(resp=="text/csv"):
        identifier= identifier + ".csv"
        writeContentToFile(identifier,response)
    else:
        if(resp=="application/json"):
            identifier=identifier + ".json"
            writeContentToFile(identifier,response)
            convertJSONtoCSV(identifier)
        else:
            return resp    
    
def writeContentToFile(file, response):
    '''Writing to file de content of the response'''
    with open(file, 'wb') as handle:
        for block in response.iter_content(1024):
            handle.write(block)

def convertJSONtoCSV(file):
    '''Converting JSON to CSV for further API generation from CSV'''    
    df = pd.read_json(file)
    df.to_csv(file, index = None)
        