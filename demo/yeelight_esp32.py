from webduino.board import *
from uyeelight import *
import time
import machine, neopixel

def findBulb():
    while True:
        bulbs = Bulb.search(timeout=2)
        if len(bulbs)==0:
            print("not found")
        else:
            break;
    return list(bulbs.keys())[0]
    
def initBulb(ip):
    print("bulb ip:",ip)
    global bulb
    bulb = Bulb(ip) 
    bulb.set_rgb(11,50,11, effect=EFFECT.SUDDEN, duration=0.1)
    bulb.turn_on()    

def initBoard():
    global np
    global bitV2
    enable = machine.Pin(2, machine.Pin.OUT)
    enable.on()
    np = neopixel.NeoPixel(machine.Pin(4), 25)    
    bitV2 = Board()
    bitV2.onTopic("ctrl",ctrl)    

def setLED(r,g,b):    
    for led in range(25):
        np[led] = (r,g,b)
    np.write()

# topic = 'light/ctrl'
def ctrl(msg):
    rgb = msg.split(' ')
    print("rgb:%s"%rgb)
    r = int(rgb[0])
    g = int(rgb[1])
    b = int(rgb[2])
    bulb.set_rgb(r,g,b, effect=EFFECT.SUDDEN, duration=0.1)
    bulb.turn_on()
    setLED(r,g,b)
    
def main():
    # init board , connect to wifi
    initBoard()
    setLED(5,0,0)
    # find bulb's IP
    ip = findBulb()
    setLED(0,0,5)
    # init bulb
    initBulb(ip)
    setLED(0,5,0)
    # check mqtt
    bitV2.loop()
    
    
main()
