import subprocess
import pandas as pd

## Configure file source and project properties


def generateAPI(file, format):
    """Generating API from specified file, format must be JSON or CSV"""
    ##Convert from JSON to CSV
    if(format == "JSON"):
        df = pd.read_json(file)
        df.to_csv(file, index = None)
    ##Calling API generator
    subprocess.call(['java', '-jar', 'ag.jar', 'csv2api', file])
    
    