from machine import Pin,I2C
import ssd1306


i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)  #Init i2c
display = ssd1306.SSD1306_I2C(64,48,i2c)             #create LCD object,Specify col and row

display.text("ESP8266",0,0)
display.text("test",0,16)
display.text("123456",0,32)
display.fill(0)
display.text("XXX1234",0,0)
display.show()
