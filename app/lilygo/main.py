from webduino.espnow import ESPNow
from webduino.display import Display
from machine import Pin, reset
import time

# 初始化顯示屏
ed = Display(font='/text_lite_24px_2312.v3.bmf')
ed.text("Hello", 10, 10)


# 定義 ESPNow 的回調函數 , {b'^\xcf\x7fh\xe2\xce': [-51, 293462]}
def callback(peer,msg,peers_table):
    print("callback")
    msg = msg.decode()
    info = [item.strip() for item in msg.split(',')]
    rssi = [values[0] for values in peers_table.values()]
    print("info:"+msg)
    print("peer:"+str(peers_table))
    if(len(info)==3):
        ed.text(f"{info[0]}: {rssi}", 5, 2)
        ed.text(f"{info[1]}", 45, 27,clear=False)
        ed.text(f"{info[2]}", 45, 50,clear=False)
        print(rssi)
    else:
        ed.text(f"{info[0]}", 5, 2)
        ed.text(f"rssi: {rssi}", 5, 27,clear=False)
        
# esp01
#esp = ESPNow(b'\x18\xfe\x34\xd7\x86\x93') # esp01 led
#esp.sendFile("./esp01.py", "./main.py", 200, callback)

# esp01 強
#esp = ESPNow(b'\x18\xfe\x34\xd7\x89\xcd')


# webbitv1
#esp = ESPNow(b'\xff\xff\xff\xff\xff\xff') # broadcast
esp = ESPNow('wbitv1')
esp.recv(callback)
esp.sendFile("./webbitv1.py", "./main.py", 200, callback)

while True:
    esp.send(b'Hello')
    print('while')
    time.sleep(0.5)



# wemos
#esp = ESPNow(b'\xbc\xff\x4d\x82\x62\x9b') # wemos matrix bc:ff:4d:82:62:9b
#esp.sendFile("./wemos_matrix.py", "./main.py", 200, callback)

#esp = ESPNow('wa1234') # 32cam
#esp.sendFile("./cam32.py", "./main.py", 200, callback)


ed.text("Send done", 10, 30)
#time.sleep(1)
#esp.cmd_reset()

# 定義按鈕的引腳和回調函數
button = Pin(0, Pin.IN, Pin.PULL_UP)

def check_button(pin):
    if pin.value() == 0:
        print('reset')
        reset()

# 設置按鈕的中斷回調
button.irq(trigger=Pin.IRQ_FALLING, handler=check_button)

