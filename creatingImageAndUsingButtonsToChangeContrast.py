#!/usr/bin/env python3#!/usr/bin/env python3
# https://shop.pimoroni.com/products/inky-impression
# script to create an image in code and display on Inky 7 Impression colour display: https://github.com/pimoroni/inky/blob/master/library/inky/inky_uc8159.py
# and then change the contrast using the buttons on the side of the Inky Impression
# https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html
# make sure to install the Pimoroni Inky libary first!
# run the following command:
# curl https://get.pimoroni.com/inky | bash
# button interaction code taken from https://github.com/pimoroni/inky/blob/master/examples/7color/buttons.py

from inky.inky_uc8159 import Inky
from PIL import Image, ImageDraw, ImageFont
import signal
import RPi.GPIO as GPIO

print("""creatingImageAndUsingButtonsToChangeContrast.py - changing contrast on a test image

Press Ctrl+C to exit!

""")

inky = Inky()

# we have 7 lovely Inky colours
colours = [inky.BLACK, inky.WHITE, inky.GREEN, inky.BLUE, inky.RED, inky.YELLOW, inky.ORANGE]

# create an image, with pink as a background colour, to see how it dithers when we draw the image to the Inky
# https://rgb.to/hotpink - #ff69b4 / rgb(255, 105, 180);
generatedImage = Image.new("RGB", (inky.width, inky.height), (255, 105, 180))

# get a font
fnt = ImageFont.truetype("SpaceGrotesk-Medium.ttf", 40)
# get a drawing context
d = ImageDraw.Draw(generatedImage)

# draw multiline text
d.multiline_text((10,10), "Hello\nWorld", font=fnt, fill=(0, 0, 0))

# Gpio pins for each button (from top to bottom)
BUTTONS = [5, 6, 16, 24]

# These correspond to buttons A, B, C and D respectively
LABELS = ['A', 'B', 'C', 'D']

# Set up RPi.GPIO with the "BCM" numbering scheme
GPIO.setmode(GPIO.BCM)

# Buttons connect to ground when pressed, so we should set them up
# with a "PULL UP", which weakly pulls the input signal to 3.3V.
GPIO.setup(BUTTONS, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# "handle_button" will be called every time a button is pressed
# It receives one argument: the associated input pin.
def handle_button(pin):
    label = LABELS[BUTTONS.index(pin)]
    print("Button press detected on pin: {} label: {}".format(pin, label))
    if label == 'A':
        inky.set_image(generatedImage, saturation=0.0)
        inky.show()
    elif label == 'B':
        inky.set_image(generatedImage, saturation=0.333)
        inky.show()
    elif label == 'C':
        inky.set_image(generatedImage, saturation=0.666)
        inky.show()
    elif label == 'D':
        inky.set_image(generatedImage, saturation=1.0)
        inky.show()
    else:
        print("Error, unknown button pressed")
        
# Loop through out buttons and attach the "handle_button" function to each
# We're watching the "FALLING" edge (transition from 3.3V to Ground) and
# picking a generous bouncetime of 250ms to smooth out button presses.
for pin in BUTTONS:
    GPIO.add_event_detect(pin, GPIO.FALLING, handle_button, bouncetime=250)

# Finally, since button handlers don't require a "while True" loop,
# we pause the script to prevent it exiting immediately.
signal.pause()