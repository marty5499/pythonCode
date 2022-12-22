import machine, neopixel
p = machine.Pin(2)
n = neopixel.NeoPixel(p, 16)
for i in range(16):
    n[i] = (i * 1, i*2, 2)
n.write()
