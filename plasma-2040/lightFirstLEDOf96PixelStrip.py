import plasma
from plasma import plasma2040

NUM_LEDS = 96

led_strip = plasma.WS2812(NUM_LEDS, 0, 0, plasma2040.DAT)

led_strip.start()
led_strip.set_rgb(0, 255, 0, 0)