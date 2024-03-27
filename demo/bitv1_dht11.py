from webduino.webbitv1 import WebBit
from webduino.image import get_image
import time

wbit = WebBit()
pin = 2
while True:
    # eg. 23 (°C)
    print("temperature:"+str(wbit.readDHT11_temp(pin)))
    # eg. 41 (% RH)
    print("humidity:"+str(wbit.readDHT11_humi(pin)))  
    time.sleep(1)