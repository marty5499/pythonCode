from webduino.webbit import WebBit
import time

wbit = WebBit()

while True:
    temp = wbit.readTemp() # 讀取溫度數值
    num_lights_on = int(temp) # 轉換為整數
    print(num_lights_on)
    if num_lights_on < 0: # 溫度小於0時，不點亮任何燈
        num_lights_on = 0
    elif num_lights_on > 24: # 溫度大於24時，點亮所有燈
        num_lights_on = 25
    for i in range(num_lights_on):
        wbit.show(i, temp*50, 0, 0) # 紅色的值為溫度數值*50
    for i in range(num_lights_on, 25):
        wbit.show(i, 0, 0, 0) # 其他燈關閉
    time.sleep(0.1) # 每隔0.1秒讀取一次溫度數值
