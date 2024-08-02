esp = ESPNow()
esp.recv(callback)

# 傳送檔案到指定節點
peer = '18:fe:34:d7:86:93' # esp01_dht_module
peer = '3c:71:bf:2f:5c:b5' # wemos 容錯測試
peer = '18:fe:34:d7:90:3d' # esp01_dht_module
peer = 'bc:ff:4d:4a:99:21' # wemos 時鐘
peer = '5c:cf:7f:22:01:51' # wemos ssd1306
peer = '5c:cf:7f:81:00:6e' # smart (60)
peer = '5c:cf:7f:81:05:3c' # smart (61)
peer = '5c:cf:7f:81:00:0f' # smart (62) 光感
peer = '5c:cf:7f:d3:26:ab' # smart + 4x Matrix

ed.text('Ready...', 10, 10)
def sendFileReport(peer_mac_str , sendBytes , total_length):
    print(f"{peer_mac_str}: {sendBytes} / {total_length}")
    ed.text(peer_mac_str, 10, 10)
    ed.text("sendFile", 10, 30, clear=False)
    ed.text(f"size: {sendBytes} / {total_length}", 10, 60, clear=False)

esp.join(peer) # 加入節點
#esp.sendCmd(ESPNow.CMD_ACK, peer)
esp.sendSyncFile(peer, "./app.py", "./main.py", 200, sendFileReport)
# 更新程式褲
#esp.sendSyncFile(peer, "./lib/webduino/espnow_8266.py", "./lib/webduino/espnow_8266.py", 200, sendFileReport)
esp.sendCmd(ESPNow.CMD_RST, peer) # 讓節點重新開機
