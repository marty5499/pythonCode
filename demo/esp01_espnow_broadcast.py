from machine import Pin
import time, espnow, ubinascii, network, machine, urandom

# 获取并显示 MAC 地址
mac = network.WLAN().config('mac')
mac_str = ubinascii.hexlify(mac, ':').decode()
print("MAC Address:", mac_str)

def init_espnow():
    global e
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    e = espnow.ESPNow()
    e.active(True)
    e.add_peer(b'\xff\xff\xff\xff\xff\xff')
    print("init espnow ok")


def generate_random_number():
    return ''.join([str(urandom.getrandbits(4) % 10) for _ in range(10)])

init_espnow()
e.send(b'\xff\xff\xff\xff\xff\xff', generate_random_number())
print("1 send...")
