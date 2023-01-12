import machine
import max7219
from time import sleep
from machine import Pin, SoftSPI

sleep(1.5)
#spi = SPI(1,100000)
spi = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=Pin(0), mosi=Pin(2), miso=Pin(15))

display = max7219.Matrix8x8(spi,Pin(3,Pin.OUT), 1)

#DIN = MOSI = machine.Pin(13)
#CLK = SCK = machine.Pin(14)
#CS = MISO = machine.Pin(15)
while True:

    display.fill(1)
    display.show()
    sleep(0.5)

    for letter in '0123456789':
        display.fill(0)
        print(letter)
        display.text(letter,0,1)
        display.show()
        sleep(0.2)


