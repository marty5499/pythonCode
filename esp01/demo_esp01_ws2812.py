import machine, neopixel
import time, ubinascii, network, machine
from machine import Pin

# Mac
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
print("[MAC] " + mac)

time.sleep(3)

p = machine.Pin(2)
n = neopixel.NeoPixel(p, 64)

# red
def show(r,g,b):
    for i in range(64):
        n[i] = (r,g,b)
    n.write()


def love():
    heart_pattern = [
        0, 0, 1, 0, 0, 1, 0, 0,
        0, 1, 1, 1, 1, 1, 1, 0,
        1, 1, 1, 1, 1, 1, 1, 1,
        1, 1, 1, 1, 1, 1, 1, 1,
        0, 1, 1, 1, 1, 1, 1, 0,
        0, 0, 1, 1, 1, 1, 0, 0,
        0, 0, 0, 1, 1, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0
    ]
    r, g, b = 2, 0, 0  # 紅色愛心
    for i in range(64):
        if heart_pattern[i] == 1:
            n[i] = (r, g, b)
        else:
            n[i] = (0, 0, 0)
    n.write()


def broadcast(val):
    show(val*3,0,0)
    esp.broadcast(mac)
    time.sleep(0.5)

def callback(peer,msg):
    if msg == b'red':
        show(3,0,0)
    if msg == b'green':
        show(0,3,0)
    if msg == b'blue':
        love()

broadcast(1)
broadcast(0)
broadcast(1)
esp.recv(callback)
show(0,0,3)

while True:
    esp.irecv(1)

