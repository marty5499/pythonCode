from webduino.espnow import ESPNow
from webduino.display import Display
from machine import Pin, reset
import time

# 初始化顯示屏 
ed = Display(font='/text_lite_24px_2312.v3.bmf')
ed.text("Hello", 10, 10)

# 初始化 ESPNow
#esp = ESPNow('wa1234')
esp = ESPNow('wa1234') # broadcast b'\x18\xfe\x34\xd7\x86\x93'

# 定義 ESPNow 的回調函數
def callback(peer,msg):
    ed.text(msg.decode(), 10, 30)
    print(msg)

esp.recv(callback)

# 發送檔案
#esp.sendFile("./esp01.py", "./main.py", 200, callback)
#time.sleep(3)
#print("reset..")
#esp.cmd_reset()

# 定義按鈕的引腳和回調函數
button = Pin(0, Pin.IN, Pin.PULL_UP)

def check_button(pin):
    if pin.value() == 0:
        print('reset')
        reset()

# 設置按鈕的中斷回調
button.irq(trigger=Pin.IRQ_FALLING, handler=check_button)



