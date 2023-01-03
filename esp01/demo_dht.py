import dht , machine
from machine import Pin

pin0 = Pin(0,Pin.OUT)
pin0.value(1)

def dht11():
    dht11 = dht.DHT11(machine.Pin(2))
    dht11.measure()
    temp = dht11.temperature() # eg. 23 (°C)
    humi = dht11.humidity()
    print("temp:%s , humi:%s"%(temp,humi))

def dht22():
    dht22 = dht.DHT22(machine.Pin(2))
    dht22.measure()
    temp = dht22.temperature() # eg. 23 (°C)
    humi = dht22.humidity()
    print("temp:%s , humi:%s"%(temp,humi))


dht22()
