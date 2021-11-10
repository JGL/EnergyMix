import time
import picounicorn
import json
try:
    import xmltok  # https://pypi.org/project/micropython-xmltok/
    import io
except ImportError:
    xmltok = None
from micropython import const

try:
    import ppwhttp
except ImportError:
    raise RuntimeError("Cannot find ppwhttp. Have you copied ppwhttp.py to your Pico?")
 
try:
    from secrets import XML_ENERGY_EXCEPT_SOLAR_REQUEST_PATH
except ImportError:
    XML_ENERGY_EXCEPT_SOLAR_REQUEST_PATH = None

"""
EnergyMix uses the Pico Unicorn Pack for the RPI Pico to display energy mix information
https://shop.pimoroni.com/products/pico-unicorn-pack
"""

picounicorn.init()

w = picounicorn.get_width()
h = picounicorn.get_height()

for x in range(w):
    for y in range(h):
        picounicorn.set_pixel(x, y, 255, 0, 0)

#new request every hour?
HTTP_REQUEST_DELAY = const(60*60)
#HTTP_REQUEST_PORT = const(80)
# 443 as we are going via https
HTTP_REQUEST_PORT = const(443)
XML_ENERGY_EXCEPT_SOLAR_REQUEST_HOST = "api.bmreports.com"

JSON_SOLAR_REQUEST_HOST = "api0.solar.sheffield.ac.uk"
JSON_SOLAR_REQUEST_PATH = "/pvlive/api/v3/ggd/0"

#put in some default data for the energy types in MW and their colours
solarMW = 10.0
solarColourTuple = (231, 222, 35)
gasMW = 10.0
gasColourTuple = (216, 123, 36)
coalMW = 10.0
coalColourTuple = (28, 24, 28)
nuclearMW = 10.0
nuclearColourTuple = (205, 36, 37)
windMW = 10.0
windColourTuple = (255, 255, 255)
pumpedStorageHydroMW = 10.0
nonPumpedHydroMW = 10.0
hydroMW = pumpedStorageHydroMW + nonPumpedHydroMW
hydroColourTuple = (30, 29, 174)
biomassMW = 10.0
biomassColourTuple = (29, 173, 35)
totalEnergyUsage = 0.0

energyPalette = [solarColourTuple, gasColourTuple, coalColourTuple, nuclearColourTuple, windColourTuple, hydroColourTuple, biomassColourTuple]
energyDescriptors = ['Solar', 'Gas', 'Coal', 'Nuclear', 'Wind', 'Hydro', 'Biomass']
energyUsages = [solarMW, gasMW, coalMW, nuclearMW, windMW, hydroMW, biomassMW]
#create an empty array to hold the lengths of LED pixels for each of the energy usages
lengthsInLEDPixels = []

def calculateTotalEnergyUsage():
    global energyUsages, totalEnergyUsage, solarMW, gasMW, coalMW, nuclearMW, windMW, hydroMW, biomassMW
    
    #make sure the energyUsages array is empty!
    energyUsages.clear()
    #make sure the totalEnergyUsage is 0
    totalEnergyUsage = 0
    
    energyUsages = [solarMW, gasMW, coalMW, nuclearMW, windMW, hydroMW, biomassMW]
    for currentEnergy in energyUsages:
        totalEnergyUsage = totalEnergyUsage + currentEnergy
    print("Total energy: ", totalEnergyUsage)

def calculateNumberOfPixelsForEachPowerSource():
    global lengthsInLEDPixels, energyUsages, totalEnergyUsage
    
    # make sure it's empty!
    lengthsInLEDPixels.clear()
    
    for currentEnergy in energyUsages:
        currentEnergyRatio = currentEnergy / totalEnergyUsage
        currentShareAsLength = currentEnergyRatio * (w-1)
        # casting to integer ignores everyting after decimal point
        lengthsInLEDPixels.append(int(currentShareAsLength))
    
    print("energyUsages are: {}".format(energyUsages))
    print("lengthsInLEDPixels are: {}".format(lengthsInLEDPixels))

def drawEnergyMix():
    global lengthsInLEDPixels, energyPalette
    
    calculateTotalEnergyUsage()
    calculateNumberOfPixelsForEachPowerSource()

    for y in range(h):
        startingLEDOnStrip = 0
        currentListIndex = 0
        
        for LEDLength in lengthsInLEDPixels:
            redValue = energyPalette[currentListIndex][0]
            greenValue = energyPalette[currentListIndex][1]
            blueValue = energyPalette[currentListIndex][2]
        
            for x in range(startingLEDOnStrip, startingLEDOnStrip+LEDLength):
                picounicorn.set_pixel(x, y, redValue, greenValue, blueValue)
        
            #increment starting LED pixel position and indexing variable
            startingLEDOnStrip = startingLEDOnStrip+LEDLength
            currentListIndex = currentListIndex+1

#just draw initially with the fake data to check the ratios look correct
drawEnergyMix()

ppwhttp.start_wifi()
ppwhttp.set_dns(ppwhttp.GOOGLE_DNS)

# Get our own local IP!
my_ip = ppwhttp.get_ip_address()
print("Local IP: {}.{}.{}.{}".format(*my_ip))

def XMLEnergyExceptSolarHandler(head, body):
    global gasMW, coalMW, nuclearMW, windMW, pumpedStorageHydroMW, nonPumpedHydroMW, hydroMW, biomassMW
    if xmltok is not None:
        # if head["Status"] == "200 OK":
        # since the server doesn't return a Status header, I guess it's safe to assume no status == OK
        data = xmltok.tokenize(io.StringIO(body))
        currentSolarMW = float(xmltok.text_of(data, "currentMW"))
        gasMW = float(xmltok.text_of(data, "currentMW"))
        print("gasMW is: {}".format(gasMW))
        
        unusedOCGTMW = float(xmltok.text_of(data, "currentMW"))
        unusedOILMW = float(xmltok.text_of(data, "currentMW"))
        
        coalMW = float(xmltok.text_of(data, "currentMW"))
        print("coalMW is: {}".format(coalMW))
        
        nuclearMW = float(xmltok.text_of(data, "currentMW"))
        print("nuclearMW is: {}".format(nuclearMW))
        
        windMW = float(xmltok.text_of(data, "currentMW"))
        print("windMW is: {}".format(windMW))
        
        pumpedStorageHydroMW = float(xmltok.text_of(data, "currentMW"))
        print("pumpedStorageHydroMW is: {}".format(pumpedStorageHydroMW))
        
        nonPumpedHydroMW = float(xmltok.text_of(data, "currentMW"))
        print("nonPumpedHydroMW is: {}".format(nonPumpedHydroMW))
        
        hydroMW = pumpedStorageHydroMW + nonPumpedHydroMW
        print("hydroMW is: {}".format(hydroMW))
        
        unusedOTHERMW = float(xmltok.text_of(data, "currentMW"))
        unusedINTFR = float(xmltok.text_of(data, "currentMW"))
        unusedINTIRL = float(xmltok.text_of(data, "currentMW"))
        unusedINTNED = float(xmltok.text_of(data, "currentMW"))
        unusedINTEW = float(xmltok.text_of(data, "currentMW"))
        
        biomassMW = float(xmltok.text_of(data, "currentMW"))
        print("biomassMW is: {}".format(biomassMW))
        drawEnergyMix()
    else:
        print("Unable to parse API response!")
        return
        
def JSONSolarHandler(head, body):
    global solarMW
#     if head["Status"] == "200 OK":
# since the server doesn't return a Status header, and I guess it's safe to assume no status == OK
    # Parse as JSON
    data = json.loads(body)
    print("JSON is: {}".format(data))
    solarMW = float(data["data"][0][3])
    print("solarMW is: {}".format(solarMW))
    drawEnergyMix()
        

while True:
# had to double timeout to 10,000 ms as the XML server is throttled/slow it seems
    ppwhttp.http_request(XML_ENERGY_EXCEPT_SOLAR_REQUEST_HOST, HTTP_REQUEST_PORT, XML_ENERGY_EXCEPT_SOLAR_REQUEST_HOST, XML_ENERGY_EXCEPT_SOLAR_REQUEST_PATH, XMLEnergyExceptSolarHandler, timeout=10000, connection_mode=ppwhttp.TLS_MODE)
    ppwhttp.http_request(JSON_SOLAR_REQUEST_HOST, HTTP_REQUEST_PORT, JSON_SOLAR_REQUEST_HOST, JSON_SOLAR_REQUEST_PATH, JSONSolarHandler, connection_mode=ppwhttp.TLS_MODE)
    time.sleep(HTTP_REQUEST_DELAY)
