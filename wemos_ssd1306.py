from machine import Pin,I2C
import ssd1306
 
i2c = I2C(scl=Pin(5), sda=Pin(4), freq=100000)  #Init i2c
 
lcd=ssd1306.SSD1306_I2C(64,48,i2c)             #create LCD object,Specify col and row
lcd.text("ESP8266",0,0)                        
lcd.text("test",0,16)                       
lcd.text("123456",0,32)                        
lcd.show()