esp = ESPNow()
esp.recv(callback)

# 傳送檔案到指定節點
ed.text('18:fe:34:ca:cc:2b', 10, 10)
ed.text("sendFile: hello.py", 10, 30, clear=False)
def onMsg(peer_mac_str , sendBytes , total_length):
    print(f"{peer_mac_str}: {sendBytes} / {total_length}")
    ed.text('18:fe:34:ca:cc:2b', 10, 10)
    ed.text("sendFile: hello.py", 10, 30, clear=False)
    ed.text(f"{sendBytes} / {total_length}", 10, 60, clear=False)
#esp.sendSyncFile('18:fe:34:ca:cc:2b', "./lib/webduino/espnow.py", "./xxx.py", 200, onMsg)
esp.sendSyncFile('18:fe:34:ca:cc:2b', "./hello.py", "./hello_3.py", 200, onMsg)

#esp.join("18:fe:34:d7:86:93") # esp01_93 溫濕度偵測
#esp.sendFile("./app_esp01_dht_module.py", "./main.py", 200, callback)
# esp.cmd_reset()

"""
while True:
    esp.send(b'red')
    time.sleep(0.1)
    esp.send(b'blue')
    time.sleep(0.1)
    esp.send(b'green')
    time.sleep(0.1)
"""