from webduino.board import *
from uyeelight import *
import time
import machine, neopixel

enable = machine.Pin(2, machine.Pin.OUT)
enable.on()

np = neopixel.NeoPixel(machine.Pin(4), 25)

def setLED(r,g,b):    
    for led in range(25):
        np[led] = (r,g,b)
    np.write()

setLED(5,0,0)

bitV2 = Board()
setLED(0,5,0)

# topic = 'yeelight/ctrl'
def ctrl(msg):
    rgb = msg.split(' ')
    print("rgb:%s"%rgb)
    setLED(int(rgb[0]),int(rgb[1]),int(rgb[2]))
    

bitV2.onTopic("ctrl",ctrl)
bitV2.loop()



