# Unicorn pack playing

import picounicorn

"""
EnergyMix uses the Pico Unicorn Pack for the RPI Pico to display energy mix information
https://shop.pimoroni.com/products/pico-unicorn-pack
"""

picounicorn.init()
w = picounicorn.get_width()
h = picounicorn.get_height()

# https://www.pyblog.in/programming/print-formmating-in-python/#Stringformat_method
print("The width is of the unicorn is {0}, the height of the unicorn is {1}".format(w,h))

def setAllUnicornLEDsBlack():
    for x in range(w):
        for y in range(h):
            picounicorn.set_pixel(x, y, 0, 0, 0)

print("Setting all pixels to black")
setAllUnicornLEDsBlack()

print("Press Button A to continue to the next demo")

while not picounicorn.is_pressed(picounicorn.BUTTON_A):  # Wait for Button A to be pressed
    pass

setAllUnicornLEDsBlack()
print("After setting black, setting pixels red starting from 0,1 then continuing x, x+1")

#sort this out!

picounicorn.set_pixel(0, 1, 255, 0, 0)
picounicorn.set_pixel(1, 2, 255, 0, 0)
picounicorn.set_pixel(2, 3, 255, 0, 0)
picounicorn.set_pixel(3, 4, 255, 0, 0)
picounicorn.set_pixel(4, 5, 255, 0, 0)
picounicorn.set_pixel(5, 6, 255, 0, 0)
            
print("Press Button B to continue to the next demo")

while not picounicorn.is_pressed(picounicorn.BUTTON_B):  # Wait for Button B to be pressed
    pass

setAllUnicornLEDsBlack()
print("After setting black, setting whole row to red")
for x in range(w):
     picounicorn.set_pixel(x, 0, 255, 0, 0)
     
print("Press Button X to continue to the next demo")

while not picounicorn.is_pressed(picounicorn.BUTTON_X):  # Wait for Button X to be pressed
    pass

setAllUnicornLEDsBlack()
print("After setting black, setting whole column to red")
for y in range(h):
    picounicorn.set_pixel(0, y, 255, 0, 0)