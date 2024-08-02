import network
import espnow

# 啟用 WLAN STA 接口
sta = network.WLAN(network.STA_IF)
sta.active(True)

# 初始化 ESPNow 並啟用
e = espnow.ESPNow()
e.active(True)

# 加入對等節點
peer = b'\xbc\xff\x4d\x82\x62\x9b'  # wemos
e.add_peer(peer)

print("add peer")


# 接收消息
host, msg = e.recv()
if msg:
    print("Received message from", host, ":", msg)

# 獲取 RSSI
print(e.peers_table)