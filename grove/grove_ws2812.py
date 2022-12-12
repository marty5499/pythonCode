import machine, neopixel
p = machine.Pin(2)
n = neopixel.NeoPixel(p, 4)
for i in range(4):
    n[i] = (i * 20+10, i*2, 22)
n.write()
