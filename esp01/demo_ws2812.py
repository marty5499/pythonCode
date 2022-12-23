import machine, neopixel
p = machine.Pin(0)
n = neopixel.NeoPixel(p, 16)
for i in range(16):
    n[i] = (i * 20+10, i*2, 22)
n.write()
