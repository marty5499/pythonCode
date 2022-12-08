import time, espnow, time, ubinascii, network, machine
from machine import Pin,I2C

 
led = Pin(2,Pin.OUT)
led.value(0)
e = None

# Reset wifi to AP_IF off, STA_IF on and disconnected
def init_espnow():
    global e
    sta = network.WLAN(network.STA_IF); sta.active(False)
    ap = network.WLAN(network.AP_IF); ap.active(False)
    sta.active(True)
    while not sta.active():
        time.sleep(1)

    sta.disconnect()   # For ESP8266
    while sta.isconnected():
        time.sleep(1)
    
    sta.active(False)
    ap.active(True)
    print("init espnow")
    e = espnow.ESPNow()
    e.active(True)
    e.add_peer(network.WLAN().config('mac'))

def send(state,i):
    e.send(b'\xff\xff\xff\xff\xff\xff', mac)
    led.value(state)
    time.sleep(0.15)

mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
time.sleep(1.5)
led.value(1)
print("[MAC] " + mac)
init_espnow()

send(0,1)
send(1,2)
