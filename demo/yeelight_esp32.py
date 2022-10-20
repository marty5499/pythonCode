from webduino.board import *
from uyeelight import *
import time
import machine, neopixel

enable = machine.Pin(2, machine.Pin.OUT)
enable.on()

np = neopixel.NeoPixel(machine.Pin(18), 25)

def setLED(r,g,b):    
    for led in range(25):
        np[led] = (r,g,b)
    np.write()

setLED(5,0,0)

bitV2 = Board(devId='yeelight')

setLED(0,0,5)

while True:
    bulbs = Bulb.search(timeout=2)
    if len(bulbs)==0:
        print("not found")
    else:
        break;

setLED(0,5,0)

# topic = 'yeelight/ctrl'
def ctrl(msg):
    rgb = msg.split(' ')
    print("rgb:%s"%rgb)
    bulb.set_rgb(int(rgb[0]),int(rgb[1]),int(rgb[2]), effect=EFFECT.SUDDEN, duration=0.1)
    bulb.turn_on()
    bulb.set_rgb(int(rgb[0]),int(rgb[1]),int(rgb[2]), effect=EFFECT.SUDDEN, duration=0.1)
    bulb.turn_on()
    bulb.set_rgb(int(rgb[0]),int(rgb[1]),int(rgb[2]), effect=EFFECT.SUDDEN, duration=0.1)
    bulb.turn_on()
    setLED(int(rgb[0]),int(rgb[1]),int(rgb[2]))
    

bitV2.onTopic("ctrl",ctrl)

ip = list(bulbs.keys())[0]


print("bulb ip:",ip)
bulb = Bulb(ip) 
bulb.set_rgb(11,50,11, effect=EFFECT.SUDDEN, duration=0.1)
bulb.turn_on()


bitV2.loop()

