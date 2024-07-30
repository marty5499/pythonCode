from machine import Pin
import time, espnow, ubinascii, network, machine
import dht

time.sleep(3)

# 获取并显示 MAC 地址
mac = network.WLAN().config('mac')
mac_str = ubinascii.hexlify(mac, ':').decode()
print("MAC Address:", mac_str)

# 初始化 DHT22 感測器
dht_pin = Pin(2)  # 使用 GPIO2 作為 DHT22 的數據引腳
dht_sensor = dht.DHT22(dht_pin)

def init_espnow():
    global e
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    if not sta.active():
        raise RuntimeError("Failed to activate STA interface")
    print("STA interface activated")

    try:
        e = espnow.ESPNow()
        e.active(True)
        e.add_peer(b'\xff\xff\xff\xff\xff\xff')
        print("init espnow ok")
    except Exception as ex:
        print("Failed to initialize ESPNow:", ex)

def broadcast(msg):
    try:
        e.send(b'\xff\xff\xff\xff\xff\xff', msg)
        print("broadcasting...")
    except Exception as ex:
        print("Failed to broadcast:", ex)

def read_dht_sensor():
    try: 
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temperature, humidity
    except Exception as ex:
        print("Failed to read from DHT sensor:", ex)
        return None, None

init_espnow()
print("ready...")

while True:
    temperature, humidity = read_dht_sensor()
    if temperature is not None and humidity is not None:
        msg = "71, {:.1f} C, {:.1f} %".format(temperature, humidity)
        broadcast(msg)
        print("send:", msg)
    time.sleep(2)  # 每 2 秒讀取並廣播一次
