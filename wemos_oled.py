from webduino.board import Board
from machine import Pin,I2C
import time, ssd1306

# ssd1306
i2c = I2C(scl=Pin(4), sda=Pin(5), freq=100000) #wemos
lcd = ssd1306.SSD1306_I2C(128,64,i2c) #create LCD object,Specify col and row
lcd.text("ESP8266",0,0)                        
lcd.show()

"""
# wemos
wemos = Board()

def execEval(topic,msg):
    topic = topic.decode("utf-8")
    msg = msg.decode("utf-8")
    print('topic:',topic,' ,msg:',msg)
    if(topic == 'display'):
        eval(msg)
        lcd.show()

print("start...")
wemos.mqtt.sub('wabaord/state',execEval)
wemos.loop()

"""