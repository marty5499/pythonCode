import machine,neopixel
np = neopixel.NeoPixel(machine.Pin(18), 25)

def setLED(r,g,b):    
    for led in range(25):
        np[led] = (r,g,b)
    np.write()

setLED(4,4,1)

print("OK")