import random
import time
import src.floworchestrator 

#Choosing a random topic from the list
with open("tests/topics.txt", "r") as file:
    topics = file.readlines()
#Select random topic or setting one static    
#selectedTopic= random.choice(topics).strip()
selectedTopic= "Transportation"
print("The selected topis is: " + selectedTopic)

#Configuring the input source 
testInit = src.floworchestrator.MainController("tests/config.properties")

#Reading data from specified source
projects = testInit.readDatafromSource(selectedTopic)

#Parse the JSON file to DCAT Catalogue
start = time.time()
testInit.mapMetadata(projects)

# Persist catalog serialized as Turtle
testInit.generateRDFoutput('tests/catalogue_output.ttl')

end = time.time()
print("The time of execution of above program is :", end-start)
