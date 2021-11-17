# This is a version of Energy Mix for the Unicorn Pack without any connectivity
# Fake as in the data is manually created, rather than retrieved live from the web

import picounicorn
import random
import math

"""
EnergyMix uses the Pico Unicorn Pack for the RPI Pico to display energy mix information
https://shop.pimoroni.com/products/pico-unicorn-pack
"""

picounicorn.init()

unicornWidth = picounicorn.get_width()
unicornHeight = picounicorn.get_height()

# https://www.pyblog.in/programming/print-formmating-in-python/#Stringformat_method
print("The width is of the unicorn is {0}, the height of the unicorn is {1}".format(unicornWidth,unicornHeight))

def setAllUnicornLEDsBlack():
    for x in range(unicornWidth):
        for y in range(unicornHeight):
            picounicorn.set_pixel(x, y, 0, 0, 0)

#for x in range(w):
#    for y in range(h):
#        picounicorn.set_pixel(x, y, 255, 0, 0)

#put in some default data for the energy types in MW and their colours
solarMW = random.uniform(0, 100) #10.0
# yellow
solarColourTuple = (255, 255, 0)
gasMW = random.uniform(0, 100) #10.0
# purple
gasColourTuple = (128, 0, 128)
coalMW = random.uniform(0, 100) #10.0
# slate grey
coalColourTuple = (112, 128, 144)
nuclearMW = random.uniform(0, 100) #10.0
# green
nuclearColourTuple = ((0, 128, 0))
windMW = random.uniform(0, 100) #10.0
# white
windColourTuple = (255, 255, 255)
pumpedStorageHydroMW = random.uniform(0, 100) #10.0
nonPumpedHydroMW = random.uniform(0, 100) #10.0
hydroMW = pumpedStorageHydroMW + nonPumpedHydroMW
# blue
hydroColourTuple = (0, 0, 255)
biomassMW = random.uniform(0, 100) #10.0
# brown
biomassColourTuple = (139, 69, 19)
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
    
    indexToEnergyDescriptor = 0
    
    # https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
    for index, currentEnergy in enumerate(energyUsages):
        currentEnergyRatio = currentEnergy / totalEnergyUsage
        currentShareAsLength = currentEnergyRatio * (unicornWidth-1)
        # casting to integer ignores everything after decimal point, not casting any more
        # lengthsInLEDPixels.append(int(currentShareAsLength))
        # https://www.w3schools.com/python/ref_func_round.asp
        currentShareAsLengthRounded = round(currentShareAsLength)
        currentShareAsLengthFloored = math.floor(currentShareAsLength)
        currentShareAsLengthCeiled = math.ceil(currentShareAsLength)
        lengthsInLEDPixels.append(currentShareAsLengthRounded)
        print("currentEnergyRatio for {0} is: {1}, this translates to {2} rounded pixels (was {3} before rounding) and {4} floor and {5} ceil.".format(energyDescriptors[index], currentEnergyRatio, currentShareAsLengthRounded, currentShareAsLength, currentShareAsLengthFloored, currentShareAsLengthCeiled))
     
    print("energyDescriptors are: {}".format(energyDescriptors))
    print("energyUsages are: {}".format(energyUsages))
    print("lengthsInLEDPixels are: {}".format(lengthsInLEDPixels))

def drawEnergyMix():
    global lengthsInLEDPixels, energyPalette
    
    calculateTotalEnergyUsage()
    calculateNumberOfPixelsForEachPowerSource()

    setAllUnicornLEDsBlack()
    
    for y in range(unicornHeight):
        startingLEDOnStrip = 0
        currentListIndex = 0
        
        for index, currentLEDLength in enumerate(lengthsInLEDPixels):
            redValue = energyPalette[index][0]
            greenValue = energyPalette[index][1]
            blueValue = energyPalette[index][2]
        
            for x in range(startingLEDOnStrip, startingLEDOnStrip+currentLEDLength):
                picounicorn.set_pixel(x, y, redValue, greenValue, blueValue)
        
            #increment starting LED pixel position and indexing variable
            startingLEDOnStrip = startingLEDOnStrip+currentLEDLength

#just draw initially with the fake data to check the ratios look correct
drawEnergyMix()

