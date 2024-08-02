import espnow, ubinascii, network, machine, dht
from machine import Pin


# 初始化 DHT22 感測器 , GPIO2 作為 DHT22 的數據引腳
dht_sensor = dht.DHT22(Pin(2))
def read_dht_sensor():
    try:
        dht_sensor.measure()
        temperature = dht_sensor.temperature()
        humidity = dht_sensor.humidity()
        return temperature, humidity
    except Exception as ex:
        return -1, -1


def callback(peer,msg):
    print(msg)


esp.recv(callback)
#lilygoNode = b'\xf4\x12\xfa\x41\x3c\xf4'
#esp.e.add_peer(lilygoNode)

while True:
    temperature, humidity = read_dht_sensor()
    msg = "71, {:.1f} C, {:.1f} %".format(temperature, humidity)
    print(msg)
    esp.broadcast(msg)
    #esp.send(lilygoNode, msg)
    esp.irecv(1) # 每 1 秒讀取並廣播一次