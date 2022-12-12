###### tags: `micropython`
Heltec esp32+LoRa
====


![](/uploads/upload_5ceba17cd21b350502c807fcf599a82f.png)

![](/uploads/upload_c0f30435fe41d4073217eb66b83f45e7.png)



https://ithelp.ithome.com.tw/articles/10227249

https://escapequotes.net/heltec-esp32-display-lcd-text-micropython/

Lora
https://github.com/fantasticdonkey/uLoRa
![](/uploads/upload_183482747a0158f4750df39e504fb6b1.png)


## Test
```python=
import ssd1306
from machine import Pin, I2C
import time
import network


wlan = network.WLAN(network.STA_IF) # create station interface
wlan.active(True)       # activate the interface
wlan.isconnected()      # check if the station is connected to an AP
time.sleep_ms(500)
if not wlan.isconnected():
  print('connecting to network...')
  wlan.connect('webduino.io', 'webduino') # connect to an AP
  time.sleep_ms(500)
  while not wlan.isconnected():
    pass
print('network config:', wlan.ifconfig())

# Heltec LoRa 32 with OLED Display
oled_width = 128
oled_height = 64
# OLED reset pin
i2c_rst = Pin(16, Pin.OUT)
# Initialize the OLED display
i2c_rst.value(0)
time.sleep_ms(5)
i2c_rst.value(1) # must be held high after initialization
# Setup the I2C lines
i2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)
i2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)
# Create the bus object
i2c = I2C(scl=i2c_scl, sda=i2c_sda)
# Create the display object
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled.fill(0)
oled.text(wlan.ifconfig()[0], 0, 0)
oled.text('HELLO WiFi ESP32', 0, 25)
oled.text('escapequotes.net', 0, 55)
  
#oled.line(0, 0, 50, 25, 1)
oled.show()
```


## SSD1306

```python=
from machine import Pin, I2C, SPI
import ssd1306, time, network
from sx127x import SX127x


OnboardLED = Pin(25, Pin.OUT)

time.sleep(1)
OnboardLED.value(not OnboardLED.value())
time.sleep(1)
OnboardLED.value(not OnboardLED.value())



class heltec:
    def init():
        ###
        heltec.device_config = {'miso':19,'mosi':27,'ss':18,'sck':5,'dio_0':35,'reset':14,'led':2}
        heltec.lora_parameters = {
            'frequency': 868E6, 'tx_power_level': 2, 
            'signal_bandwidth': 125E3,  'spreading_factor': 8, 
            'coding_rate': 5, 'preamble_length': 8,
            'implicit_header': False,'sync_word': 0x12, 
            'enable_CRC': False,'invert_IQ': False,
        }
        heltec.device_spi = SPI(baudrate=10000000,
                polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
                sck = Pin(heltec.device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
                mosi = Pin(heltec.device_config['mosi'], Pin.OUT, Pin.PULL_UP),
                miso = Pin(heltec.device_config['miso'], Pin.IN, Pin.PULL_UP))
        heltec.lora = SX127x(heltec.device_spi, pins=heltec.device_config, parameters=heltec.lora_parameters)        
        # Heltec LoRa 32 with OLED Display
        heltec.oled_width = 128
        heltec.oled_height = 64
        # OLED reset pin
        heltec.i2c_rst = Pin(16, Pin.OUT)
        # Initialize the OLED display
        heltec.i2c_rst.value(0)
        time.sleep_ms(5)
        heltec.i2c_rst.value(1) # must be held high after initialization
        # Setup the I2C lines
        heltec.i2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)
        heltec.i2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)
        # Create the bus object
        heltec.i2c = I2C(scl=heltec.i2c_scl, sda=heltec.i2c_sda)
        # Create the display object
        heltec.oled = ssd1306.SSD1306_I2C(heltec.oled_width, heltec.oled_height, heltec.i2c)        
        
    def fill(n):
        heltec.oled.fill(n)
        heltec.oled.show()
        
    def text(str,x,y):
        heltec.oled.text(str,x,y)
        heltec.oled.show()
        
    def line(x1,y1,x2,y2,bold):
        heltec.oled.line(x1,y1,x2,y2, bold)
        heltec.oled.show()


def receive(lora):
    print("LoRa Receiver")
    while True:
        if lora.received_packet():
            lora.blink_led()
            payload = lora.read_payload()
            heltec.fill(0)
            heltec.text('LoRa init...', 20, 5)
            heltec.text(payload, 20, 25)

heltec.init()
receive(heltec.lora)
heltec.text('LoRa init...', 20, 5)

```


## Sender

```python=
from machine import Pin, I2C, SPI
import ssd1306, time, network
from sx127x import SX127x


OnboardLED = Pin(25, Pin.OUT)

time.sleep(1)
OnboardLED.value(not OnboardLED.value())
time.sleep(1)
OnboardLED.value(not OnboardLED.value())



class heltec:
    def init():
        ###
        heltec.device_config = {'miso':19,'mosi':27,'ss':18,'sck':5,'dio_0':35,'reset':14,'led':2}
        heltec.lora_parameters = {
            'frequency': 868E6, 'tx_power_level': 2, 
            'signal_bandwidth': 125E3,  'spreading_factor': 8, 
            'coding_rate': 5, 'preamble_length': 8,
            'implicit_header': False,'sync_word': 0x12, 
            'enable_CRC': False,'invert_IQ': False,
        }
        heltec.device_spi = SPI(baudrate=10000000,
                polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
                sck = Pin(heltec.device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
                mosi = Pin(heltec.device_config['mosi'], Pin.OUT, Pin.PULL_UP),
                miso = Pin(heltec.device_config['miso'], Pin.IN, Pin.PULL_UP))
        heltec.lora = SX127x(heltec.device_spi, pins=heltec.device_config, parameters=heltec.lora_parameters)        
        # Heltec LoRa 32 with OLED Display
        heltec.oled_width = 128
        heltec.oled_height = 64
        # OLED reset pin
        heltec.i2c_rst = Pin(16, Pin.OUT)
        # Initialize the OLED display
        heltec.i2c_rst.value(0)
        time.sleep_ms(5)
        heltec.i2c_rst.value(1) # must be held high after initialization
        # Setup the I2C lines
        heltec.i2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)
        heltec.i2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)
        # Create the bus object
        heltec.i2c = I2C(scl=heltec.i2c_scl, sda=heltec.i2c_sda)
        # Create the display object
        heltec.oled = ssd1306.SSD1306_I2C(heltec.oled_width, heltec.oled_height, heltec.i2c)        
        
    def fill(n):
        heltec.oled.fill(n)
        heltec.oled.show()
        
    def text(str,x,y):
        heltec.oled.text(str,x,y)
        heltec.oled.show()
        
    def line(x1,y1,x2,y2,bold):
        heltec.oled.line(x1,y1,x2,y2, bold)
        heltec.oled.show()


def send(lora):
    counter = 0
    while True:
        payload = 'Hello ({0})'.format(counter)
        heltec.fill(0)
        heltec.text("Send:{}".format(payload),5,20)
        lora.println(payload)
        counter += 1
        time.sleep(0.5)

heltec.init()
heltec.text('LoRa send...', 20, 5)
send(heltec.lora)
```


## Receiver


```python=
from machine import Pin, I2C, SPI
import ssd1306, time, network
from sx127x import SX127x


OnboardLED = Pin(25, Pin.OUT)

time.sleep(1)
OnboardLED.value(not OnboardLED.value())
time.sleep(1)
OnboardLED.value(not OnboardLED.value())



class heltec:
    def init():
        ###
        heltec.device_config = {'miso':19,'mosi':27,'ss':18,'sck':5,'dio_0':35,'reset':14,'led':2}
        heltec.lora_parameters = {
            'frequency': 868E6, 'tx_power_level': 2, 
            'signal_bandwidth': 125E3,  'spreading_factor': 8, 
            'coding_rate': 5, 'preamble_length': 8,
            'implicit_header': False,'sync_word': 0x12, 
            'enable_CRC': False,'invert_IQ': False,
        }
        heltec.device_spi = SPI(baudrate=10000000,
                polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
                sck = Pin(heltec.device_config['sck'], Pin.OUT, Pin.PULL_DOWN),
                mosi = Pin(heltec.device_config['mosi'], Pin.OUT, Pin.PULL_UP),
                miso = Pin(heltec.device_config['miso'], Pin.IN, Pin.PULL_UP))
        heltec.lora = SX127x(heltec.device_spi, pins=heltec.device_config, parameters=heltec.lora_parameters)        
        # Heltec LoRa 32 with OLED Display
        heltec.oled_width = 128
        heltec.oled_height = 64
        # OLED reset pin
        heltec.i2c_rst = Pin(16, Pin.OUT)
        # Initialize the OLED display
        heltec.i2c_rst.value(0)
        time.sleep_ms(5)
        heltec.i2c_rst.value(1) # must be held high after initialization
        # Setup the I2C lines
        heltec.i2c_scl = Pin(15, Pin.OUT, Pin.PULL_UP)
        heltec.i2c_sda = Pin(4, Pin.OUT, Pin.PULL_UP)
        # Create the bus object
        heltec.i2c = I2C(scl=heltec.i2c_scl, sda=heltec.i2c_sda)
        # Create the display object
        heltec.oled = ssd1306.SSD1306_I2C(heltec.oled_width, heltec.oled_height, heltec.i2c)        
        
    def fill(n):
        heltec.oled.fill(n)
        heltec.oled.show()
        
    def text(str,x,y):
        heltec.oled.text(str,x,y)
        heltec.oled.show()
        
    def line(x1,y1,x2,y2,bold):
        heltec.oled.line(x1,y1,x2,y2, bold)
        heltec.oled.show()


def receive(lora):
    print("LoRa Receiver")
    while True:
        if lora.received_packet():
            lora.blink_led()
            payload = lora.read_payload()
            heltec.fill(0)
            heltec.text('LoRa init...', 20, 5)
            heltec.text(payload, 20, 25)

heltec.init()
receive(heltec.lora)
heltec.text('LoRa init...', 20, 5)
```