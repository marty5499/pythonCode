from webduino.webbit import WebBit
import time
strong = 50
colors = [(0, 0, strong), (strong, 0, 0), (0, strong, 0), (strong, strong, 0)] # 藍、紅、綠、黃色循環
interval = 0.005 # 燈間隔速度
wbit = WebBit()

def rainbow():
    i = 0
    while True:
        wbit.show(i % 25, *colors[i // 25 % len(colors)]) # 控制webbit 25顆燈七彩流水燈方式呈現
        time.sleep(interval)
        i += 1

rainbow()
