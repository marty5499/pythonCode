import time, espnow, time, ubinascii, network, machine
from machine import Pin,I2C
import ssd1306


led = Pin(2,Pin.OUT)
led.value(0)

class OLED:
    
    def init():
        i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)  #Init i2c
        OLED.lcd = ssd1306.SSD1306_I2C(64,48,i2c) #create LCD object,Specify col and row
        OLED.show(0,0,"ESP8266")

    def show(x,y,text):
        OLED.lcd.text(text,x,y)
        OLED.lcd.show()
    
    def clear():
        OLED.lcd.fill(0)
        OLED.lcd.show()

# Reset wifi to AP_IF off, STA_IF on and disconnected
def init_espnow():
    global e
    sta = network.WLAN(network.STA_IF); sta.active(False)
    ap = network.WLAN(network.AP_IF); ap.active(False)
    sta.active(True)
    while not sta.active():
        time.sleep(0.1)
    sta.disconnect()   # For ESP8266
    while sta.isconnected():
        time.sleep(0.1)
    e = espnow.ESPNow()
    e.active(True)
    e.add_peer(network.WLAN().config('mac'))

def send(state,i):
    OLED.show(5,10, "send..%d" % i)
    e.send(b'\xff\xff\xff\xff\xff\xff', mac)
    led.value(state)
    time.sleep(0.15)
    OLED.clear()

OLED.init()
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
OLED.show(0,30,mac)
time.sleep(1.5)
led.value(1)
print("[MAC] " + mac)
OLED.clear()
e = None
mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
init_espnow()

for i in range(1,4):
    send(0,i)
    send(1,i)
    
OLED.clear()


OLED.show(0,0,"waiting...")
while True:
    host, msg = e.irecv()
    OLED.clear()
    if msg:
        msg = msg.decode('utf-8')
        OLED.show(0,20,msg)
