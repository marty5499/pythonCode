from webduino.webbitv1 import WebBit  
import time

wbit = WebBit()
wbit.setPin(0,True)
time.sleep(1)
wbit.setPin(0,False)
