import time
from webduino.image import get_image
from webduino.webbit import WebBit

def ctrl(topic,cmd):
    print(">> "+cmd)

wbit = WebBit()
wbit.connect()
wbit.sub('myctrl',ctrl)
print("init...ok")

while True: 
    wbit.checkMsg()
    # 偵測按鈕狀態
    if wbit.btnA():  # 只按下A
      wbit.matrix(0, 100, 0, get_image("arrow_right"))  # 顯示綠色右三角形
      ctrl("myctrl","192.168.0.4 0 on") #打開插座
      ctrl("myctrl","192.168.0.4 1 on")
      ctrl("myctrl","192.168.0.4 2 on")
    if wbit.btnB():  # 只按下B
      wbit.matrix(100, 0, 0, get_image("arrow_left"))  # 顯示紅色左三角形
      ctrl("myctrl","192.168.0.4 0 off") #關閉插座
      ctrl("myctrl","192.168.0.4 1 off")
      ctrl("myctrl","192.168.0.4 2 off")