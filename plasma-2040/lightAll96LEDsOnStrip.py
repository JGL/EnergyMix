import plasma
from plasma import plasma2040

NUM_LEDS = 96

led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma2040.DAT)

led_strip.start()

for i in range(NUM_LEDS):
    led_strip.set_rgb(i, 127, 0, 0)