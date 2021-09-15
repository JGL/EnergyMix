from plasma import plasma2040
from pimoroni import RGBLED

led = RGBLED(plasma2040.LED_R, plasma2040.LED_G, plasma2040.LED_B)

# lets make the onboard LED go green!
led.set_rgb(0, 255, 0)