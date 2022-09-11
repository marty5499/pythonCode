from uyeelight import *
from machine import Pin,I2C
from webduino.board import Board

# esp01
esp01 = Board(devId='0314')
#esp01.connect("KingKit_2.4G","webduino")
"""
while True:
    bulbs = Bulb.search(timeout=2)
    if len(bulbs)==0:
        print("not found")
    else:
        break;
    
ip = list(bulbs.keys())[0]
print("bulb ip:",ip)
bulb = Bulb(ip) 
bulb.turn_on()
bulb.set_rgb(255,255,255, effect=EFFECT.SUDDEN, duration=0.1)
"""
bulb = Bulb("192.168.0.52")
bulb.turn_on()
bulb.set_rgb(11,2,2,duration=1)