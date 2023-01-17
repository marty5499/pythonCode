from machine import Pin
from time import sleep

red = Pin(0,Pin.OUT)
green = Pin(2,Pin.OUT)
flag = True

for i in range(0,20):
    if flag==True:
        red.value(1)
        green.value(1)
    else:
        red.value(0)
        green.value(0)
    flag = not flag
    print(flag)
    sleep(0.5)

    