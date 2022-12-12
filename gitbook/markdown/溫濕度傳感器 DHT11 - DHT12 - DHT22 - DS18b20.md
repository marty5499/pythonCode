###### tags: `micropython`
溫濕度傳感器 DHT11 / DHT12 / DHT22 / DS18b20
========







### esp01 dht11
![](/uploads/upload_4b85808d857ccb74b73f8796244dd7a5.png =40%x)

```python=
import network, time, machine, ubinascii, os
import usocket, ntptime, random
from machine import Pin, PWM, Timer, WDT
from umqtt.simple import MQTTClient
import dht


class debug:
    def print(msg="",msg2="",msg3=""):
        print("[debug]",msg,msg2,msg3)
        pass

class WiFi:

    def ip():
        print(Wifi.sta.ifconfig())
        
    def check():
        print(WiFi.sta.isconnected())

    def disconnect():
        WiFi.sta.disconnect()

    def checkConnection():
        debug.print("wifi state:",WiFi.sta.isconnected())
        if not WiFi.sta.isconnected():
            debug.print("connect broke ! retry...")
            WiFi.connect()
            debug.print("!!!! online callback... !!!!")

    def setup(ssid="webduino.io",pwd="webduino"):
        WiFi.ssid = ssid
        WiFi.pwd = pwd

    def connect():
        WiFi.sta = sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        debug.print('connecting WiFi:',WiFi.ssid,WiFi.pwd)
        cnt = 0
        sta_if.connect(WiFi.ssid,WiFi.pwd)
        while not sta_if.isconnected():
            cnt = cnt + 1
            time.sleep(0.5)
            if cnt == 10:
                cnt = 0
                debug.print("retry connect...")
        WiFi.ip = sta_if.ifconfig()[0];
        return True

class MQTT():

    def setup(server = 'mqtt1.webduino.io',user ='webduino' ,pwd='webduino',keepalive=60):
        MQTT.user = user
        MQTT.pwd = pwd
        MQTT.server = server
        userId = 'guest'#+str(random.randint(0,10000))
        MQTT.client = MQTTClient(userId, MQTT.server, user=MQTT.user, password=MQTT.pwd)
        MQTT.connectState = False
    
    def connect():
        while MQTT.connectState is not True:
            MQTT.connectState = True if MQTT.client.connect() == 0 else False
            time.sleep(1)
        try:
            MQTT.subTopic
            debug.print("resubscribe:",MQTT.subTopic)
            MQTT.sub(MQTT.subTopic,MQTT.callback)
        except:
            pass
        
    def pub(topic,msg):
        try:
            MQTT.client.publish(topic,msg)
        except OSError as e:
            print("reconnecting...")
            MQTT.client.connect(False)
            MQTT.sub(MQTT.subTopic,MQTT.callback)
            print("reconected.")

    def sub(topic,cb):
        MQTT.subTopic = topic
        MQTT.callback = cb
        MQTT.client.set_callback(cb)
        MQTT.client.subscribe(topic)

    def checkMsg():
        try:
            MQTT.client.check_msg()
        except OSError as e:
            print("reconnecting...")
            MQTT.client.connect(False)
            MQTT.sub(MQTT.subTopic,MQTT.callback)
            print("reconected.")

class ESP01():
    
    def init():
        ESP01.wifi = WiFi
        ESP01.mqtt = MQTT
        ESP01.wifi.setup('KingKit_2.4G','webduino')
        ESP01.mqtt.setup('mqtt1.webduino.io','webduino','webduino')
        
        
    def connect():
        ESP01.wifi.connect()
        debug.print("wifi connected.")
        ESP01.mqtt.connect()
        debug.print("mqtt connected.")


class DHT11App:
    
    def init(name):
        DHT11App.name = str.encode(name)
        DHT11App.esp01 = ESP01
        DHT11App.dht11 = dht.DHT11(machine.Pin(2))
        DHT11App.esp01.init()
        DHT11App.esp01.connect()

    def read():
        DHT11App.dht11.measure()
        DHT11App.temp = DHT11App.dht11.temperature() # eg. 23 (°C)
        DHT11App.humi = DHT11App.dht11.humidity()    # eg. 41 (% RH)
    
    def sim():
        DHT11App.temp = 1
        DHT11App.humi = 2

    def run():
        now = 0
        min = 10
        enableDeepSleepMode = 0
        while True:
            #DHT11App.sim()
            if now % 100 == 0:
                DHT11App.esp01.mqtt.client.ping()
            if now == min or now == 0:
                print("Trigger....")
                now = 0
                try:
                    DHT11App.esp01.wifi.checkConnection()
                    DHT11App.read()
                    info = str(DHT11App.temp)+" "+str(DHT11App.humi)
                    print("pub:",info)
                    DHT11App.esp01.mqtt.pub((DHT11App.name+b'/state'), str.encode(info))
                    print("ok")
                except Exception as e:
                    print("DHT11App exception:",e)
            # enter deepsleep 5min
            if enableDeepSleepMode > 0:
                print("deep sleep:",enableDeepSleepMode,'mins')
                machine.deepsleep(enableDeepSleepMode*60*1000)
            DHT11App.esp01.mqtt.checkMsg()
            time.sleep(0.1)
            now = now + 1

DHT11App.init("dht11")
DHT11App.run()
```




### DHT22

![](/uploads/upload_17929c83990641fa11453b5fb268e072.png)

```python=
import dht,time
from machine import Pin
from webduino.board import Board

sensor = dht.DHT22(Pin(2))

def measure():
    sensor.measure()
    return str(sensor.temperature())+" "+str(sensor.humidity())

try:
    print("==")
    print("-=-=-=-= base =-=-=-=-")
    print("==")
    board = Board(devId='dht22')
    while True:
        time.sleep(3)
        board.publish("sroom/data", measure())
        board.check()
except Exception as e:
    print(e)
    print('')
    machine.reset()

```


![](/uploads/upload_07050c99c1da3863fc1be04daaee94eb.png =30%x)

```python=
import network, time, machine, ubinascii, os
import usocket, ntptime, random
from machine import Pin, PWM, Timer, WDT
from umqtt.simple import MQTTClient
import machine, onewire, ds18x20, time
#import dht


class debug:
    def print(msg="",msg2="",msg3=""):
        print("[debug]",msg,msg2,msg3)
        pass

class WiFi:

    def ip():
        print(Wifi.sta.ifconfig())
        
    def check():
        print(WiFi.sta.isconnected())

    def disconnect():
        WiFi.sta.disconnect()

    def checkConnection():
        debug.print("wifi state:",WiFi.sta.isconnected())
        if not WiFi.sta.isconnected():
            debug.print("connect broke ! retry...")
            WiFi.connect()
            debug.print("!!!! online callback... !!!!")

    def setup(ssid="webduino.io",pwd="webduino"):
        WiFi.ssid = ssid
        WiFi.pwd = pwd

    def connect():
        WiFi.sta = sta_if = network.WLAN(network.STA_IF)
        sta_if.active(True)
        debug.print('connecting WiFi:',WiFi.ssid,WiFi.pwd)
        cnt = 0
        sta_if.connect(WiFi.ssid,WiFi.pwd)
        while not sta_if.isconnected():
            cnt = cnt + 1
            time.sleep(0.5)
            if cnt == 10:
                cnt = 0
                debug.print("retry connect...")
        WiFi.ip = sta_if.ifconfig()[0];
        return True

class MQTT():

    def setup(server = 'mqtt1.webduino.io',user ='webduino' ,pwd='webduino',keepalive=60):
        MQTT.user = user
        MQTT.pwd = pwd
        MQTT.server = server
        userId = 'guest'#+str(random.randint(0,10000))
        MQTT.client = MQTTClient(userId, MQTT.server, user=MQTT.user, password=MQTT.pwd)
        MQTT.connectState = False
    
    def connect():
        while MQTT.connectState is not True:
            MQTT.connectState = True if MQTT.client.connect() == 0 else False
            time.sleep(1)
        try:
            MQTT.subTopic
            debug.print("resubscribe:",MQTT.subTopic)
            MQTT.sub(MQTT.subTopic,MQTT.callback)
        except:
            pass
        
    def pub(topic,msg):
        try:
            MQTT.client.publish(topic,msg)
        except OSError as e:
            print("reconnecting...")
            MQTT.client.connect(False)
            MQTT.sub(MQTT.subTopic,MQTT.callback)
            print("reconected.")

    def sub(topic,cb):
        MQTT.subTopic = topic
        MQTT.callback = cb
        MQTT.client.set_callback(cb)
        MQTT.client.subscribe(topic)

    def checkMsg():
        try:
            MQTT.client.check_msg()
        except OSError as e:
            print("reconnecting...")
            MQTT.client.connect(False)
            MQTT.sub(MQTT.subTopic,MQTT.callback)
            print("reconected.")

class ESP01():
    
    def init():
        ESP01.wifi = WiFi
        ESP01.mqtt = MQTT
        ESP01.wifi.setup('KingKit_2.4G','webduino')
        ESP01.mqtt.setup('mqtt1.webduino.io','webduino','webduino')
        
        
    def connect():
        ESP01.wifi.connect()
        debug.print("wifi connected.")
        ESP01.mqtt.connect()
        debug.print("mqtt connected.")


class DS18B20:
    
    def init(name):
        DS18B20.name = str.encode(name)
        DS18B20.esp01 = ESP01
        DS18B20.sensor = ds18x20.DS18X20(onewire.OneWire(machine.Pin(3)))
        DS18B20.roms = DS18B20.sensor.scan()
        DS18B20.sensor.convert_temp()
        DS18B20.esp01.init()
        DS18B20.esp01.connect()

    def run():
        now = 0
        min = 10
        enableDeepSleepMode = 0
        while True:
            if now % 100 == 0:
                DS18B20.esp01.mqtt.client.ping()
            if now == min or now == 0:
                print("Trigger....")
                now = 0
                try:
                    DS18B20.esp01.wifi.checkConnection()
                    for rom in DS18B20.roms:
                        info = str(rom)+" "+str(DS18B20.sensor.read_temp(rom))
                        DS18B20.esp01.mqtt.pub((DS18B20.name+b'/state'), str.encode(info))
                    print("ok")
                except Exception as e:
                    print("DS18B20 exception:",e)
            DS18B20.esp01.mqtt.checkMsg()
            time.sleep(0.1)
            now = now + 1

DS18B20.init("ds18b20")
DS18B20.esp01.mqtt.pub((DS18B20.name+b'/state'), str.encode("Start..."))
DS18B20.run()

```