# Tool for FAIR data production (DCAT metadata adoption + Web APIs generation)
This project is for development FAIRification process (i.e. make CS initiatives more FAIR compliant) which maps metadata of CS platforms' catalogues to DCAT and generates Web Application Programming Interfaces (APIs) for improving CS data discoverability and reusability in an integrated approach. 

## How to use
1. Clone the code
2. Install requirements usin pip (python version > 3.8)
3. Set up the catalogue metadata input in the *config.properties* file. The properties file contains a description, catalogue URL, and the source of projects metadata. 
4. Run *flowOchestrator* class. 
Then, the projects are retrieved from the source specified in the file, could be a local file or a remote endpoint. 
Once metadata is retrieved, the class \textit{mMpScistarterCatalogue} (implementation of the \textit{MapCatalogue} interface) maps the metadata fields from Scistarter to DCAT.
5. If you need to redefine the mapper, you must extend the class *MapCatalogue*.
6. During the mapper execution if data raw is available by metadata reference, the *APIfication* (which is a Java suproccess) is launched, generating *Web API* packages for the corresponding data. The Web APIs packages are called following the pattern AG_projectID
7. Then, once Web APIs are generated and published, the specification of data services is thus added to the DCAT metadata *Catalogue*.
8. Finally, this *Catalogue* is serialized in Turtle and could be shared as RDF linked data.

## Sample & tests
The folder *tests* contains a basic configuration to execute an example.
The class *generatejson* generates retrieves a ramdon number of projects querying the SciStarter API by the topics specified in the file *topics.txt*. 
The time of execution is printed in the terminal. Also a file with the catalogue is generated in the same folder. If some project fails during the mapping due to the completeness of required metadata, the identifier is also printed.

