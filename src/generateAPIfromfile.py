import subprocess
import pandas as pd

## Configure file source and project properties


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