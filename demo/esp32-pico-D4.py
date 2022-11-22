import time
import machine, neopixel
from webduino.board import *

np = neopixel.NeoPixel(machine.Pin(2), 25)

def setLED(r,g,b):    
    for led in range(25):
        np[led] = (r,g,b)
    np.write()
 
setLED(0,1,0)
print('done.')
