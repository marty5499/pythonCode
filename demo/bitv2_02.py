from webduino.webbit import WebBit
import time

wbit = WebBit()

# 發出beep一聲 
wbit.play([262,0.5])

while True:
    # 每隔0.1秒讀取溫度數值
    temp = wbit.readTemp()
    print("Temperature: {} C".format(temp))
    
    # 讀取溫度數值並點亮燈
    if 0 <= temp <= 24:
        light_num = int(temp)
        color_value = temp * 50
        wbit.show(0, color_value, 0, 0)  # 紅色
        
        # 點亮指定數量的燈
        for i in range(light_num):
            wbit.show(i, color_value, 0, 0)
        
        # 切換熄滅燈色
        for i in range(light_num + 1, 25):
             wbit.show(i,0,0,0)

    else:
        wbit.showAll(0,0,0)
    
    #等待0.1秒再進入下一個迴圈
    time.sleep(0.1)
