from webduino import *
from uyeelight import *
from machine import Pin,I2C
from utime import ticks_us, ticks_diff
from array import array
from RFBtn import RFBtn
import time,os
 
#####################
try:
    import cmd
    machine.reset()
except:
    pass
#####################

time.sleep(3)

def beep(t=1):
    beep = Pin(4,Pin.OUT)
    for i in range(t):
        beep.on()
        time.sleep(0.05)
        beep.off()
        time.sleep(0.05)


def ctrlBulb(cmd):
    print("cmd:",cmd)
    beep(1)
    eval(cmd)

def btnTrigger(code):
    print("btnCode:",code)
    if code == btn315_red:
        wemos32.mqtt.pub("wa5499/bulb","bulb.set_rgb(255,2,2,duration=1)")
    if code == btn315_blue:
        wemos32.mqtt.pub("wa5499/bulb","bulb.set_rgb(2,2,255,duration=1)")
    if code == btn315_yellow:
        wemos32.mqtt.pub("wa5499/bulb","bulb.set_rgb(255,255,2,duration=1)")

btn315_blue   = "659aaaaa5959"
btn315_red    = "6559a6996959"
btn315_yellow = "556a6555a959"

# crete wemos
wemos32 = Board('yeelight')
wemos32.connect("webduino.io","webduino")
wemos32.onMsg('wa5499/btn',btnTrigger)
wemos32.onMsg("wa5499/bulb",ctrlBulb)

# create bulb
bulb = Bulb("192.168.0.95")
bulb.turn_on()
bulb.set_rgb(255,2,2,duration=1)

# create RFBtn
pin13 = Pin(13,Pin.IN)

print("start...",wemos32.deviceId)
beep(1)

while True:
    try:
        data = RFBtn.listener(pin13,wemos32.check)
        if(len(data)==12):
            wemos32.mqtt.pub("wa5499/btn",data)
    except Exception as e:
        print(e)

