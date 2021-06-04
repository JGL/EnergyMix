#!/usr/bin/env python3#!/usr/bin/env python3
# https://shop.pimoroni.com/products/inky-impression
# script to create an image in code and display on Inky 7 Impression colour display: https://github.com/pimoroni/inky/blob/master/library/inky/inky_uc8159.py
# https://pillow.readthedocs.io/en/stable/reference/ImageDraw.html

# make sure to install the Pimoroni Inky libary first!
# run the following command:
# curl https://get.pimoroni.com/inky | bash
# for more information: https://shop.pimoroni.com/products/inky-impression
from inky.inky_uc8159 import Inky

from PIL import Image, ImageDraw, ImageFont

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

saturation = 0.5
inky.set_image(generatedImage, saturation=saturation)
inky.show()

