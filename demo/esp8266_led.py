from machine import Pin
import time

p0 = Pin(2, Pin.OUT)

for i in range(10):
    time.sleep(0.25)
    p0.value(i%2)