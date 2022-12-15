from machine import Pin,I2C
import ssd1306

i2c = I2C(0, scl=Pin(18), sda=Pin(19), freq=400000)
lcd=ssd1306.SSD1306_I2C(128,64,i2c) #create LCD object,Specify col and row
lcd.text("ESP32c3",0,0)
lcd.text("test OK",0,16)
lcd.text("123456",0,32)
lcd.show()

