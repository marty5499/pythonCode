
import time
from webduino.webbitv1 import WebBit
from webduino.image import get_image
from hs300 import HS300

def ctrl(topic,cmd):
    print(">> "+cmd)
    ip, port, state = cmd.split()
    hs300 = HS300(ip)
    hs300.connect()
    port = int(port)
    state = 1 if state.lower() == 'on' else 0
    success = hs300.sw(port, state)
    resp = f'Set port {port} to {"on" if state == 1 else "off"}: {success}'
    wbit.pub('qqqq',resp)
    hs300.close()

# 積木控制 https://webbit.webduino.io/blockly/#XROzmw7Ye1oyn
wbit = WebBit()
wbit.connect()
wbit.sub('mybit',ctrl)
print("init...ok")
    
while True:
    wbit.checkMsg()
    # 偵測按鈕狀態
    if wbit.btnA():  # 只按下A
      wbit.matrix(0, 100, 0, get_image("arrow_right"))  # 顯示綠色右三角形
      ctrl("mybit","192.168.0.4 0 on") #打開插座
      ctrl("mybit","192.168.0.4 1 on")
      ctrl("mybit","192.168.0.4 2 on")
    if wbit.btnB():  # 只按下B
      wbit.matrix(100, 0, 0, get_image("arrow_left"))  # 顯示紅色左三角形
      ctrl("mybit","192.168.0.4 0 off") #關閉插座
      ctrl("mybit","192.168.0.4 1 off")
      ctrl("mybit","192.168.0.4 2 off")



