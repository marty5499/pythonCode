from webduino.display import Display
# 初始化顯示屏
ed = Display(font='/text_lite_16px_2312.v3.bmf')
ed.text("Start...", 10, 10)

from webduino.espnow import ESPNow
from machine import Pin, reset
import time
onMsg = None

def callback(peer , msg , peers_table):
    msg = msg.decode()
    print(f"msg:{msg}")
    info = [item.strip() for item in msg.split(',')]
    rssi = [values[0] for values in peers_table.values()]
    #print(f"recv[{msg}], {str(peers_table)}")
    if(len(info)==3):
        ed.text(f"{info[0]}: {rssi}", 5, 2)
        ed.text(f"{info[1]}", 45, 27,clear=False)
        ed.text(f"{info[2]}", 45, 50,clear=False)
        print(rssi)
    else:
        ed.text(f"{info[0]}", 5, 2)
        ed.text(f"rssi: {rssi}", 5, 27,clear=False)

    if not onMsg == None:
        onMsg(peer, msg, peers_table)


# 定義按鈕的引腳和回調函數
button = Pin(0, Pin.IN, Pin.PULL_UP)

def check_button(pin):
    if pin.value() == 0:
        print('reset')
        reset()

# 設置按鈕的中斷回調
button.irq(trigger=Pin.IRQ_FALLING, handler=check_button)