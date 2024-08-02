from machine import Pin, SPI
import max7219

spi = SPI(1, baudrate=10000000)
screen = max7219.Max7219(32, 8, spi, Pin(15))
screen.fill(0)
screen.show()
screen.text(' OK ', 0, 0, 1)
screen.show()

def onMsg(peer, data):
    data = data.decode()
    screen.fill(0)
    screen.text(data, 0, 0, 1)
    screen.show()

esp.recv(onMsg)
while True: esp.irecv(1)