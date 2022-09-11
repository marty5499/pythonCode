from machine import UART
import machine
import time


uart = UART(0, 115200)
on =  b'\xA0\x01\x01\xA2'
off =  b'\xA0\x01\x00\xA1'
uart.init(115200, bits=8, parity=None, stop=1)

time.sleep(2) 

def swOn():
    #ed.on()
    uart.write(on)
    time.sleep(1)
    
def swOff():
    #led.off()
    uart.write(off)
    time.sleep(1)

for i in range(1,6):
    swOn()
    swOff()


