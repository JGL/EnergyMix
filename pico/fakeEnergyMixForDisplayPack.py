# This is a version of Energy Mix for the Display Pack without any connectivity
# Fake as in the data is manually created, rather than retrieved live from the web

import picodisplay as display  # Comment this line out to use PicoDisplay2
# import picodisplay2 as display  # Uncomment this line to use PicoDisplay2
import time
import random
import math

"""
EnergyMix uses the Display Pack 1.0 for the RPI Pico to display energy mix information
https://shop.pimoroni.com/products/pico-display-pack
https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/pico_display
"""

displayWidth = display.get_width()
displayHeight = display.get_height()

display_buffer = bytearray(displayWidth * displayHeight * 2)  # 2-bytes per pixel (RGB565)
display.init(display_buffer)

display.set_backlight(1.0)

# https://www.pyblog.in/programming/print-formmating-in-python/#Stringformat_method
print("The width is of the display pack is {0}, the height of the display pack is {1}".format(displayWidth, displayHeight))

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
lengthsInPixels = []

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
    global lengthsInPixels, energyUsages, totalEnergyUsage
    
    # make sure it's empty!
    lengthsInPixels.clear()
    
    indexToEnergyDescriptor = 0
    
    # https://stackoverflow.com/questions/522563/accessing-the-index-in-for-loops
    for index, currentEnergy in enumerate(energyUsages):
        currentEnergyRatio = currentEnergy / totalEnergyUsage
        currentShareAsLength = currentEnergyRatio * (displayWidth-1)
        # casting to integer ignores everything after decimal point, not casting any more
        # lengthsInLEDPixels.append(int(currentShareAsLength))
        # https://www.w3schools.com/python/ref_func_round.asp
        currentShareAsLengthRounded = round(currentShareAsLength)
        currentShareAsLengthFloored = math.floor(currentShareAsLength)
        currentShareAsLengthCeiled = math.ceil(currentShareAsLength)
        lengthsInPixels.append(currentShareAsLengthRounded)
        print("currentEnergyRatio for {0} is: {1}, this translates to {2} rounded pixels (was {3} before rounding) and {4} floor and {5} ceil.".format(energyDescriptors[index], currentEnergyRatio, currentShareAsLengthRounded, currentShareAsLength, currentShareAsLengthFloored, currentShareAsLengthCeiled))
     
    print("energyDescriptors are: {}".format(energyDescriptors))
    print("energyUsages are: {}".format(energyUsages))
    print("lengthsInLEDPixels are: {}".format(lengthsInPixels))

def drawEnergyMix():
    global lengthsInPixels, energyPalette
    
    calculateTotalEnergyUsage()
    calculateNumberOfPixelsForEachPowerSource()

    display.clear()
    
    for y in range(displayHeight):
        startingPixelOnDisplay = 0
        currentListIndex = 0
        
        for index, currentLength in enumerate(lengthsInPixels):
            redValue = energyPalette[index][0]
            greenValue = energyPalette[index][1]
            blueValue = energyPalette[index][2]
            display.set_pen(redValue, greenValue, blueValue)
        
            for x in range(startingPixelOnDisplay, startingPixelOnDisplay+currentLength):
                display.pixel(x, y)
        
            #increment starting pixel position
            startingPixelOnDisplay = startingPixelOnDisplay+currentLength
            
    display.update() 

#just draw initially with the fake data to check the ratios look correct
drawEnergyMix()


