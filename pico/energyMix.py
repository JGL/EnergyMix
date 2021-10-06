import time
import plasma
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
 
"""
This uses the Plasma WS2812 LED library to drive a string of LEDs alongside the built-in RGB LED.
You should wire your LEDs to VBUS/GND and connect the data pin to pin 27 (unused by Pico Wireless).
See https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/plasma for the API
"""
NUM_LEDS = 96  # Number of connected LEDs
LED_PIN = 27   # LED data pin (27 is unused by Pico Wireless)
LED_PIO = 0    # Hardware PIO (0 or 1)
LED_SM = 0     # PIO State-Machine (0 to 3)

led_strip = plasma.WS2812(NUM_LEDS, LED_PIO, LED_SM, LED_PIN)
led_strip.start()
#just lighting up whole strip purple for now
for i in range(NUM_LEDS):
    led_strip.set_rgb(i, 255, 0, 255)

#new request every hour?
HTTP_REQUEST_DELAY = const(60*60)
#HTTP_REQUEST_PORT = const(80)
# 443 as we are going via https
HTTP_REQUEST_PORT = const(443)
XML_ENERGY_EXCEPT_SOLAR_REQUEST_HOST = "api.bmreports.com"
XML_ENERGY_EXCEPT_SOLAR_REQUEST_PATH = "/BMRS/FUELINSTHHCUR/v1?APIKey=po7f83ilmq2p223&ServiceType=XML"
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

def calculateTotalEnergyUsage():
    global energyUsages
    global totalEnergyUsage
    for currentEnergy in energyUsages:
        totalEnergyUsage = totalEnergyUsage + currentEnergy

calculateTotalEnergyUsage()
print("Total energy: ", totalEnergyUsage)

#create an empty array to hold the lengths of LED pixels for each of the energy usages
lengthsInLEDPixels = []

def calculateNumberOfPixelsForEachPowerSource():
    global lengthsInLEDPixels
    global energyUsages
    global totalEnergyUsage
    
    lengthsInLEDPixels = [] #make sure it's empty!
    
    for currentEnergy in energyUsages:
        currentEnergyRatio = currentEnergy / totalEnergyUsage
        currentShareAsHeight = currentEnergyRatio * (NUM_LEDS-1)
        #casting to integer ignores everyting after decimal point
        lengthsInLEDPixels.append(int(currentShareAsHeight))
        
calculateNumberOfPixelsForEachPowerSource()

def drawEnergyMix():
    global lengthsInLEDPixels
    global energyPalette
    startingLEDOnStrip = 0
    currentListIndex = 0

    for LEDLength in lengthsInLEDPixels:
        redValue = energyPalette[currentListIndex][0]
        greenValue = energyPalette[currentListIndex][1]
        blueValue = energyPalette[currentListIndex][2]
        for i in range(startingLEDOnStrip, startingLEDOnStrip+LEDLength):
            led_strip.set_rgb(i, redValue, greenValue, blueValue)
        #increment starting LED pixel position and indexing variable
        startingLEDOnStrip = startingLEDOnStrip+LEDLength
        currentListIndex = currentListIndex+1
        
drawEnergyMix()

ppwhttp.start_wifi()
ppwhttp.set_dns(ppwhttp.GOOGLE_DNS)

# Get our own local IP!
my_ip = ppwhttp.get_ip_address()
print("Local IP: {}.{}.{}.{}".format(*my_ip))

def XMLEnergyExceptSolarHandler(head, body):
#     if head["Status"] == "200 OK":
# since the server doesn't return a Status header, and I guess it's safe to assume no status == OK
        if xmltok is not None:
            # Parse as XML
            #print("Raw XML is: {}".format(body))
            data = xmltok.tokenize(io.StringIO(body))
#           color = xmltok.text_of(data, "field2")[1:]ˀ
            whatIsThis = xmltok.text_of(data, "currentMW")
            print("currentMW text of gives: {}".format(whatIsThis))
        else:
            print("Unable to parse API response!")
            return
#         r = int(color[0:2], 16)
#         g = int(color[2:4], 16)
#         b = int(color[4:6], 16)
#         ppwhttp.set_led(r, g, b)
#        print("Set LED to {} {} {}".format(r, g, b))
        #print("XML is: {}".format(data))
        
def JSONSolarHandler(head, body):
#     if head["Status"] == "200 OK":
# since the server doesn't return a Status header, and I guess it's safe to assume no status == OK
        # Parse as JSON
        data = json.loads(body)
        print("JSON is: {}".format(data))
        solarMW = float(data["data"][0][3])
        print("MW from Solar JSON is: {}".format(solarMW))
        

while True:
#     ppwhttp.http_request(HTTP_REQUEST_HOST, HTTP_REQUEST_PORT, HTTP_REQUEST_HOST, HTTP_REQUEST_PATH, handler)
#def http_request(host_address, port, request_host, request_path, handler, timeout=5000, client_sock=None, connection_mode=TCP_MODE):
# had to double timeout to 10,000 ms as the XML server is throttled/slow it seems
    ppwhttp.http_request(XML_ENERGY_EXCEPT_SOLAR_REQUEST_HOST, HTTP_REQUEST_PORT, XML_ENERGY_EXCEPT_SOLAR_REQUEST_HOST, XML_ENERGY_EXCEPT_SOLAR_REQUEST_PATH, XMLEnergyExceptSolarHandler, timeout=10000, connection_mode=ppwhttp.TLS_MODE)
    ppwhttp.http_request(JSON_SOLAR_REQUEST_HOST, HTTP_REQUEST_PORT, JSON_SOLAR_REQUEST_HOST, JSON_SOLAR_REQUEST_PATH, JSONSolarHandler, connection_mode=ppwhttp.TLS_MODE)
    time.sleep(HTTP_REQUEST_DELAY)
