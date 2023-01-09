import utime
from machine import Pin, I2C

import ahtx0

# I2C for the Wemos D1 Mini with ESP8266
#i2c = I2C(scl=Pin(0), sda=Pin(2))
i2c = I2C(scl=Pin(0), sda=Pin(2), freq=100000)

# Create the sensor object using I2C
sensor = ahtx0.AHT10(i2c)

while True:
    print("\nTemperature: %0.2f C" % sensor.temperature)
    print("Humidity: %0.2f %%" % sensor.relative_humidity)
    utime.sleep(1)