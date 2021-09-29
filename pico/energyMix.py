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
"""

NUM_LEDS = 96  # Number of connected LEDs
LED_PIN = 27   # LED data pin (27 is unused by Pico Wireless)
LED_PIO = 0    # Hardware PIO (0 or 1)
LED_SM = 0     # PIO State-Machine (0 to 3)

led_strip = plasma.WS2812(NUM_LEDS, LED_PIO, LED_SM, LED_PIN)
led_strip.start()
#just lighting up whole strip for now
for i in range(NUM_LEDS):
    led_strip.set_rgb(i, 255, 0, 255)

HTTP_REQUEST_DELAY = const(60)
# HTTP_REQUEST_PORT = const(80)
HTTP_REQUEST_PORT = const(443)
XML_ENERGY_EXCEPT_SOLAR_REQUEST_HOST = "api.bmreports.com"
XML_ENERGY_EXCEPT_SOLAR_REQUEST_PATH = "/BMRS/FUELINSTHHCUR/v1?APIKey=po7f83ilmq2p223&ServiceType=XML"
JSON_SOLAR_REQUEST_HOST = "api0.solar.sheffield.ac.uk"
JSON_SOLAR_REQUEST_PATH = "/pvlive/v2/"

ppwhttp.start_wifi()
ppwhttp.set_dns(ppwhttp.GOOGLE_DNS)

# Get our own local IP!
my_ip = ppwhttp.get_ip_address()
print("Local IP: {}.{}.{}.{}".format(*my_ip))

def XMLEnergyExceptSolarHandler(head, body):
    if head["Status"] == "200 OK":
        if xmltok is not None:
            # Parse as XML
            data = xmltok.tokenize(io.StringIO(body))
#             color = xmltok.text_of(data, "field2")[1:]ˀ
        else:
            print("Unable to parse API response!")
            return
#         r = int(color[0:2], 16)
#         g = int(color[2:4], 16)
#         b = int(color[4:6], 16)
#         ppwhttp.set_led(r, g, b)
#        print("Set LED to {} {} {}".format(r, g, b))
        print("XML is: {}".format(data))
    else:
        print("Error: {}".format(head["Status"]))
        
def JSONSolarHandler(head, body):
    if head["Status"] == "200 OK":
        # Parse as JSON
        data = json.loads(body)
#             color = data['field2'][1:]

#         r = int(color[0:2], 16)
#         g = int(color[2:4], 16)
#         b = int(color[4:6], 16)
#         ppwhttp.set_led(r, g, b)
#         print("Set LED to {} {} {}".format(r, g, b))
        print("JSON is: {}".format(data))
    else:
        print("Error: {}".format(head["Status"]))


while True:
#     ppwhttp.http_request(HTTP_REQUEST_HOST, HTTP_REQUEST_PORT, HTTP_REQUEST_HOST, HTTP_REQUEST_PATH, handler)
    ppwhttp.http_request(XML_ENERGY_EXCEPT_SOLAR_REQUEST_HOST, HTTP_REQUEST_PORT, XML_ENERGY_EXCEPT_SOLAR_REQUEST_HOST, XML_ENERGY_EXCEPT_SOLAR_REQUEST_PATH, XMLEnergyExceptSolarHandler)
    ppwhttp.http_request(JSON_SOLAR_REQUEST_HOST, HTTP_REQUEST_PORT, JSON_SOLAR_REQUEST_HOST, JSON_SOLAR_REQUEST_PATH, JSONSolarHandler)
    time.sleep(HTTP_REQUEST_DELAY)
