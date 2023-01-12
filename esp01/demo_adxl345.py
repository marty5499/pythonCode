import time, adxl345
from machine import Pin,I2C

i2c = I2C(scl=Pin(0),sda=Pin(2), freq=10000)
adx = adxl345.ADXL345(i2c)
time.sleep(1.5)

while True:
    x=adx.xValue
    y=adx.yValue
    z=adx.zValue
    #print('The acceleration info of x, y, z are:%d,%d,%d'%(x,y,z))
    roll,pitch = adx.RP_calculate(x,y,z)
    print('roll=',roll,',pitch=',pitch)
    time.sleep_ms(50)