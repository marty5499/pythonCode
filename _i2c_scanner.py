from machine import I2C, Pin

i2c = I2C(scl=Pin(4), sda=Pin(5), freq=100000) #wemos
#i2c = I2C(scl=Pin(2), sda=Pin(0), freq=100000)

print('Scan i2c bus...')
while True:
    devices = i2c.scan()
    if len(devices) == 0:
        print("No i2c device !")
    else:
      print('i2c devices found:',len(devices))
      break;

for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))
