from machine import Pin
import time
time.sleep(1)

# 無限迴圈
while True:
    #print("go")
    Pin(1, Pin.OUT).value(0)
    e.irecv(0.5)
    Pin(1, Pin.OUT).value(1)
    e.irecv(0.5)
