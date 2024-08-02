esp = ESPNow()
esp.recv(callback)

# 傳送檔案到指定節點
peer = '18:fe:34:d7:86:93' # esp01_dht_module
peer = '3c:71:bf:2f:5c:b5' # wemos 容錯測試
peer = '5c:cf:7f:d3:26:ab' # smart + 4x Matrix
peer = '18:fe:34:d7:90:3d' # esp01_dht_module
peer = 'bc:ff:4d:4a:99:21' # wemos 時鐘
peer = '5c:cf:7f:22:01:51' # wemos ssd1306
peer = '5c:cf:7f:81:00:6e' # smart (60)
peer = '5c:cf:7f:81:05:3c' # smart (61)

ed.text('Ready...', 10, 10)
#esp.join('5c:cf:7f:81:00:6e') # 加入節點
#esp.join('5c:cf:7f:81:05:3c') # 加入節點

esp.join('5c:cf:7f:d3:26:ab')
esp.sendAll('8888')
#esp.send('5c:cf:7f:d3:26:ab','1234')
#esp.sendCmd(ESPNow.CMD_ACK, peer)
#esp.sendJoin('5c:cf:7f:81:00:6e','5c:cf:7f:81:05:3c') # 傳送到指定節點
#esp.sendJoin('5c:cf:7f:81:05:3c','5c:cf:7f:81:00:6e') # 傳送到指定節點

#esp.send("0", '5c:cf:7f:81:00:6e') # 傳送到指定節點

