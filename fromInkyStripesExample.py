#!/usr/bin/env python3

# duplicated from: https://github.com/pimoroni/inky/blob/master/examples/7color/stripes.py
# make sure to install the Pimoroni Inky libary first!
# run the following command:
# curl https://get.pimoroni.com/inky | bash
# for more information: https://shop.pimoroni.com/products/inky-impression


from inky.inky_uc8159 import Inky

inky = Inky()

for y in range(inky.height - 1):
    color = y // (inky.height // 7)
    for x in range(inky.width - 1):
        inky.set_pixel(x, y, color)

inky.show()