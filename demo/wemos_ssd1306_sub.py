import ssd1306
from machine import Pin,I2C
from webduino.board import Board

i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)
display = ssd1306.SSD1306_I2C(64,48,i2c)
display.fill(0)
display.text("Init...",5,20)
display.show()

def cb(cmd):
    print(">> "+cmd)
    data = cmd.split(' ')
    display.fill(0)
    display.text("Temp:",0,0)
    display.text(data[0],20,12)
    
    display.text("Humi:",0,28)
    display.text(data[1],20,40)
    display.show()    

try:
    board = Board(devId='sroom')
    board.onTopic("data",cb)
    board.loop()
except Exception as e:
    print(e)
    machine.reset()