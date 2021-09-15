#!/usr/bin/env python3
# https://shop.pimoroni.com/products/inky-impression
# script designed for Inky 7 Impression colour display: https://github.com/pimoroni/inky/blob/master/library/inky/inky_uc8159.py
# duplicated from: https://github.com/pimoroni/inky/blob/master/examples/7color/stripes.py
# make sure to install the Pimoroni Inky libary first!
# run the following command:
# curl https://get.pimoroni.com/inky | bash
# for more information: https://shop.pimoroni.com/products/inky-impression
from inky.inky_uc8159 import Inky

#thanks to https://github.com/stchris/untangle
import untangle
xmlObj = untangle.parse('https://api.bmreports.com/BMRS/FUELINSTHHCUR/v1?APIKey=po7f83ilmq2p223&ServiceType=XML')

#thanks https://stackoverflow.com/questions/12965203/how-to-get-json-from-webpage-into-python-script
from urllib.request import urlopen
import json 

jsonURL = "https://api0.solar.sheffield.ac.uk/pvlive/v2/"
response = urlopen(jsonURL)
data = response.read().decode("utf-8")
jsonAsPythonDictionary = json.loads(data)

solarMW = float(jsonAsPythonDictionary["data"][0][2])
       
gasMW = float(xmlObj.response.responseBody.responseList.item[0].currentMW.cdata)
gasDescriptor = xmlObj.response.responseBody.responseList.item[0].fuelType.cdata

coalMW = float(xmlObj.response.responseBody.responseList.item[3].currentMW.cdata)
coalDescriptor = xmlObj.response.responseBody.responseList.item[3].fuelType.cdata

nuclearMW = float(xmlObj.response.responseBody.responseList.item[4].currentMW.cdata)
nuclearDescriptor = xmlObj.response.responseBody.responseList.item[4].fuelType.cdata

windMW = float(xmlObj.response.responseBody.responseList.item[5].currentMW.cdata)
windDescriptor = xmlObj.response.responseBody.responseList.item[5].fuelType.cdata

pumpedStorageHydroMW = float(xmlObj.response.responseBody.responseList.item[6].currentMW.cdata)
pumpedStorageHydroDescriptor = xmlObj.response.responseBody.responseList.item[6].fuelType.cdata

nonPumpedHydroMW = float(xmlObj.response.responseBody.responseList.item[7].currentMW.cdata)
nonPumpedHydroDescriptor = xmlObj.response.responseBody.responseList.item[7].fuelType.cdata

hydroMW = pumpedStorageHydroMW + nonPumpedHydroMW

biomassMW = float(xmlObj.response.responseBody.responseList.item[13].currentMW.cdata)
biomassDescriptor = xmlObj.response.responseBody.responseList.item[13].fuelType.cdata

timeLastUpdated = xmlObj.response.responseBody.dataLastUpdated.cdata

inky = Inky()

# print("Inky.colour is", inky.colour)
# print("Inky.resolution is", inky.resolution)

# we have 7 different daily energy MW usage values and we have 7 lovely Inky colours
colours = [inky.BLACK, inky.WHITE, inky.GREEN, inky.BLUE, inky.RED, inky.YELLOW, inky.ORANGE]
energyDescriptors = ['Solar', 'Gas', 'Coal', 'Nuclear', 'Wind', 'Hydro', 'Biomass']
energyUsages = [solarMW, gasMW, coalMW, nuclearMW, windMW, hydroMW, biomassMW]

totalEnergyUsage = 0.0
for currentEnergy in energyUsages:
    totalEnergyUsage = totalEnergyUsage + currentEnergy
    
print(totalEnergyUsage)

heightsInPixels = []
for currentEnergy in energyUsages:
    currentEnergyRatio = currentEnergy / totalEnergyUsage
    currentShareAsHeight = currentEnergyRatio * (inky.height-1)
    #casting to integer ignores everyting after decimal point
    heightsInPixels.append(int(currentShareAsHeight))

startingHeightOnInky = 0
currentListIndex = 0

for barHeight in heightsInPixels:
    #https://www.w3schools.com/python/ref_func_range.asp
    for y in range(startingHeightOnInky, startingHeightOnInky+barHeight):
        currentColour = colours[currentListIndex]
        for x in range(inky.width - 1):
            inky.set_pixel(x,y,currentColour)
    #increment starting bar y position and indexing variable
    startingHeightOnInky = startingHeightOnInky+barHeight
    currentListIndex = currentListIndex+1

inky.show()
