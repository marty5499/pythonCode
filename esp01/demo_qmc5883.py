from QMC5883 import QMC5883
from machine import I2C,Pin
import time

i2c = I2C(scl=Pin(0), sda=Pin(2), freq=100000)

qmc5883 = QMC5883(i2c)
qmc5883.set_sampling_rate(3)
qmc5883.set_oversampling(0)
qmc5883.set_range(1)

while True:
    x, y, z, temp = qmc5883.read_scaled()
    print("%d , %d , %d : %d" % (x,y,z,temp))
    time.sleep(0.2)
