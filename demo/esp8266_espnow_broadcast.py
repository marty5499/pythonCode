import time, espnow, time, ubinascii, network, machine
from machine import Pin

### 5c:cf:7f:81:05:3c

time.sleep(1.5)

# LED
gg = Pin(12, Pin.OUT)
bb = Pin(13, Pin.OUT)
rr = Pin(15, Pin.OUT)

# Mac
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print("[MAC] " + mac)

def rgb(r,g,b):
    gg.value(g)
    bb.value(b)
    rr.value(r)

# Reset wifi to AP_IF off, STA_IF on and disconnected
def init_espnow():
    global e
    sta = network.WLAN(network.STA_IF); sta.active(False)
    ap = network.WLAN(network.AP_IF); ap.active(False)
    sta.active(True)
    while not sta.active():
        time.sleep(0.1)
    sta.disconnect()   # For ESP8266
    while sta.isconnected():
        time.sleep(0.1)
    e = espnow.ESPNow()
    e.active(True)
    e.add_peer(network.WLAN().config('mac'))

def broadcast(r,g,b):
    rgb(r,g,b)
    e.send(b'\xff\xff\xff\xff\xff\xff', mac)
    time.sleep(0.5)

rgb(0,0,0)
init_espnow()
broadcast(1,0,0)
broadcast(0,1,0)
broadcast(0,0,1)
rgb(0,0,0)
while True:
    host, msg = e.irecv()
    if msg:
        if msg == b'red':
            rgb(3,0,0)
        if msg == b'green':
            rgb(0,3,0)
        if msg == b'blue':
            rgb(0,0,3)
        if msg == b'end':
            break
