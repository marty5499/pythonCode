import time
from webduino.webbitv1 import WebBit
wbit = WebBit()
# 設定RGB值
RED = [100, 0, 0]
GREEN = [0, 100, 0]
BLUE = [0, 0, 100]
# 呼吸燈效果
def breathe(color):
    for i in range(0, 101, 5):
        wbit.showAll(color[0]*i/100, color[1]*i/100, color[2]*i/100)
        time.sleep(0.01)
    for i in range(100, -1, -5):
        wbit.showAll(color[0]*i/100, color[1]*i/100, color[2]*i/100)
        time.sleep(0.01)
# 主要程式
for i in range(5):
    breathe(BLUE)
    breathe(GREEN)
    breathe(RED)
