import time
from webduino.webbit import WebBit

wbit = WebBit() # 初始化WebBit開發板

while True:
    left_light = wbit.leftLight() # 讀取左邊光度值
    if left_light < 300: # 如果光度值小於300
        wbit.pub('qq', str(left_light)) # 傳送光度數值到topic='qq'
        wbit.showAll(0, 100, 0) # 25顆燈都顯示綠色
    else:
        wbit.showAll(0, 0, 0) # 25顆燈都關閉

    time.sleep(0.1) # 暫停0.1秒
