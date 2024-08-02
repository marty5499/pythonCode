esp = ESPNow()
esp.recv(callback)

# 傳送檔案到指定節點
peer = '18:fe:34:d7:86:93' # esp01_dht_module
peer = '5c:cf:7f:d3:26:ab' # smart + 4x Matrix
peer = '3c:71:bf:2f:5c:b5' # wemos 容錯測試

ed.text('Ready...', 10, 10)