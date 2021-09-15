#thanks https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
from urllib.request import urlopen
import json 

jsonURL = "https://api0.solar.sheffield.ac.uk/pvlive/v2/"
response = urlopen(jsonURL)
data = response.read().decode("utf-8")
jsonAsPythonDictionary = json.loads(data)
print(jsonAsPythonDictionary)


solarMW = float(jsonAsPythonDictionary["data"][0][2])
print("SolarMW today is", solarMW)