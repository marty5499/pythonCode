Grove
=====
![](https://md.kingkit.codes/uploads/upload_2bc5ade4f9fa397925abcb905ea74fea.png =50%x)![](https://md.kingkit.codes/uploads/upload_7206733699c8780bcd0492686ceeb890.png =40%x)


## ESP01
![](https://md.kingkit.codes/uploads/upload_14b62929154ab3e6284436e1e321d2c9.png)

### Grove Pin 接法

#### 一隻訊號腳
IO0 單Pin 訊號腳

#### 兩隻訊號腳
IO0 (黃色線) <--> CLK
IO2 (白色線) <--> DIO

#### I2C
IO0 (黃色線) <--> SCL
IO2 (白色線) <--> SDA



## Scan I2C
```python=
from machine import I2C, Pin

i2c = I2C(scl=Pin(0), sda=Pin(2), freq=100000)

print('Scan i2c bus...')
while True:
    devices = i2c.scan()
    if len(devices) == 0:
        print("No i2c device !")
    else:
      print('i2c devices found:',len(devices))
      break;

for device in devices:  
    print("Decimal address: ",device," | Hexa address: ",hex(device))
```

## OLED 0.96 (64x128)
![](https://md.kingkit.codes/uploads/upload_6cd9ebf82c7387a3b2d085440b024244.png)
```python=
from machine import Pin,I2C
import ssd1306
 
i2c = I2C(scl=Pin(0), sda=Pin(2), freq=100000)  #Init i2c
lcd=ssd1306.SSD1306_I2C(128,64,i2c) #create LCD object,Specify col and row
lcd.text("ESP8266",0,0)
lcd.text("test",0,16)
lcd.text("123456",0,32)
lcd.show()
```

## Buzzer

![](https://md.kingkit.codes/uploads/upload_8a509eab66968ae4cc13c4e3724425be.png)
```python=
import machine , time

def play(freq=300,delay=0.1):
        pin25 = machine.PWM(machine.Pin(0), duty=512)
        pin25.freq(freq)
        time.sleep(delay)
        machine.PWM(machine.Pin(0), duty=0)

play(262,0.2)
play(294,0.2)
play(330,0.2)
```



## DHT11
![](https://md.kingkit.codes/uploads/upload_f0769d7a711123756a13ed915b59593c.png)


```python=
import dht , machine

dht11 = dht.DHT11(machine.Pin(0))
dht11.measure()
temp = dht11.temperature() # eg. 23 (°C)
humi = dht11.humidity()
print("temp:%s , humi:%s"%(temp,humi))
```

## TM1637
![](https://md.kingkit.codes/uploads/upload_e9592735498d944a63ee1dc5cb0641d8.png)
```python=
from TM1637 import TM1637
from machine import Pin
tm = TM1637(clk=Pin(2), dio=Pin(0))
tm.show('1234', True)  # ':' True | False
```

## WS2812
![](https://md.kingkit.codes/uploads/upload_4cb807e408eb4449cdbe0a0187807655.png)

```python=
import machine, neopixel
p = machine.Pin(0)
n = neopixel.NeoPixel(p, 4)
for i in range(4):
    n[i] = (i * 20+10, i*2, 22)
n.write()
```


### Rotary
![](https://md.kingkit.codes/uploads/upload_8b4c2b45c3c32716f93958d324c24974.png)


```python=
import time
from rotary_irq_esp import RotaryIRQ

r = RotaryIRQ(pin_num_clk=0, 
              pin_num_dt=2, 
              min_val=0, 
              max_val=5, 
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP)
              
val_old = r.value()
while True:
    val_new = r.value()
    
    if val_old != val_new:
        val_old = val_new
        print('result =', val_new)
        
    time.sleep_ms(50)
```


### HC-SR04
![](https://md.kingkit.codes/uploads/upload_570904c14c099e629afbfb66a935a10b.png)
```python=
from hcsr04 import HCSR04
from time import sleep

sensor = HCSR04(trigger_pin=0, echo_pin=2, echo_timeout_us=10000)

while True:
    distance = sensor.distance_cm()
    print('Distance:', distance, 'cm')
    sleep(1)
```


### 紅外線溫度感測
![](https://md.kingkit.codes/uploads/upload_20b52b3d83876923a599a73e596fb9a0.png)

```python=
import time
import mlx90614
from machine import I2C, Pin

i2c = I2C(scl=Pin(0), sda=Pin(2))
sensor = mlx90614.MLX90614(i2c)

while True:
    print(sensor.read_ambient_temp(), sensor.read_object_temp())
    time.sleep_ms(500)
```


### ADXL345 三軸加速
![](https://md.kingkit.codes/uploads/upload_90024f0bba4638cb6b2f52a2bee4ac1f.png)

```python=
import time, adxl345
from machine import Pin,I2C

i2c = I2C(scl=Pin(0),sda=Pin(2), freq=10000)
adx = adxl345.ADXL345(i2c)
time.sleep(1.5)

while True:
    x=adx.xValue
    y=adx.yValue
    z=adx.zValue
    #print('The acceleration info of x, y, z are:%d,%d,%d'%(x,y,z))
    roll,pitch = adx.RP_calculate(x,y,z)
    print('roll=',roll,',pitch=',pitch)
    time.sleep_ms(50)
```


### MP3 播放器 
[控制命令](https://shop.mirotek.com.tw/arduino/arduino-mini-mp3-player/)
![](https://md.kingkit.codes/uploads/upload_7a4a9a9809c1a6265ff2acb5a7832238.png)

```python=
from dfplayermini import Player
from time import sleep

music = Player()
music.volume(15)
music.play(2)
sleep(15)
music.stop() 
```

# 待測試補上範例 Code
![](https://md.kingkit.codes/uploads/upload_5eb835d603cc145a6289c54c29ee6d9f.png)

## [溫濕度](https://md.kingkit.codes/flTmxM_UQQ-FVOoThhkvqg)
![](https://md.kingkit.codes/uploads/upload_4278324ce63f23d01b7134cd46701552.png =30%x)


## [APDS-9930](https://md.kingkit.codeshttps://md.kingkit.codes/uploads/upload_f87fa3a9b43fefd1951acc414d385c46.png)

![](https://md.kingkit.codes/uploads/upload_f87fa3a9b43fefd1951acc414d385c46.png =30%x)

## [Servo](https://md.kingkit.codes/ZoEOeVAITs2dwlB25YBsAg)
![](https://md.kingkit.codes/uploads/upload_3ee8ff8b1715812e600b28c84f8e94df.png =30%x)

## [LCD1602](https://md.kingkit.codes/XCgecKh4SH6CbeR0kaMLMg)
![](https://md.kingkit.codes/uploads/upload_cdb7fb66ca7ccc300e7a0b63fc69f5c6.png)