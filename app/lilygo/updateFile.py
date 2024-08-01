esp = ESPNow()
esp.recv(callback)

# 傳送檔案到指定節點
peer_wemos_matrix = '18:fe:34:ca:cc:2b'
ed.text(peer_wemos_matrix, 10, 10)
ed.text("sendFile: hello.py", 10, 30, clear=False)

def onMsg(peer_mac_str , sendBytes , total_length):
    print(f"{peer_mac_str}: {sendBytes} / {total_length}")
    ed.text(peer_wemos_matrix, 10, 10)
    ed.text("sendFile: hello.py", 10, 30, clear=False)
    ed.text(f"size: {sendBytes} / {total_length}", 10, 60, clear=False)

#esp.sendSyncFile('18:fe:34:ca:cc:2b', "./lib/webduino/espnow.py", "./xxx.py", 200, onMsg)
esp.sendSyncFile(peer_wemos_matrix, "./wemos_matrix_main.py", "./main.py", 200, onMsg)
esp.sendCmd(ESPNow.CMD_RST, peer_wemos_matrix)
