import time, espnow, time, ubinascii, network, machine
from machine import Pin



time.sleep(1.5)

led = Pin(1,Pin.OUT)
led.value(0)
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()

def wifi_reset():   # Reset wifi to AP_IF off, STA_IF on and disconnected
  sta = network.WLAN(network.STA_IF); sta.active(False)
  ap = network.WLAN(network.AP_IF); ap.active(False)
  sta.active(True)
  while not sta.active():
      time.sleep(0.1)
  sta.disconnect()   # For ESP8266
  while sta.isconnected():
      time.sleep(0.1)
  return sta, ap

sta, ap = wifi_reset()   # Reset wifi to AP off, STA on and disconnected
peer = b'\xff\xff\xff\xff\xff\xff'  # MAC address of proxy
e = espnow.ESPNow(); e.active(True);
#e.add_peer(peer)

def send(state):
    e.send(peer, mac)
    led.value(state)
    time.sleep(1)

while True:
    send(0)
    send(1)

