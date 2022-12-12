import espnow
import machine, neopixel, network, time, ubinascii

time.sleep(1.5)

w0 = network.WLAN(network.STA_IF)
w0.active(True)

print("init...")
e = espnow.ESPNow()
e.active(True)
e.init()
peer = b'\xff\xff\xff\xff\xff\xff'
e.add_peer(peer)

np = neopixel.NeoPixel(machine.Pin(2), 25)

def setLED(r,g,b):    
    for led in range(25):
        np[led] = (r,g,b)
    np.write()
 
setLED(0,0,1)


print("wait...")
host, rcvMac = e.irecv()
rcvMac = str(rcvMac)
rcvMac = rcvMac[12:-2].replace(':','')
rmac = ubinascii.unhexlify(rcvMac)
e.add_peer(rmac)

while True:
    time.sleep(0.25)
    setLED(1,0,0)
    e.send(rmac, 'red')
    time.sleep(0.25)
    setLED(0,1,0)
    e.send(rmac, 'green')
    time.sleep(0.25)
    setLED(0,0,1)
    e.send(rmac, 'blue')


