import time, espnow, time, ubinascii, network, machine
from machine import Pin


# Mac
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print(mac)

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
    print("init espnow ok")

def broadcast():
    e.send(b'\xff\xff\xff\xff\xff\xff', mac)
    time.sleep(0.5)

init_espnow()
broadcast()

while True:
    host, msg = e.irecv()
    print(msg)
