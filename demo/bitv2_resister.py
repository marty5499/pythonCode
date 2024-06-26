from webduino.webbit import WebBit
import math
wbit = WebBit()
while True:
    # 讀取pin0可變電阻數值
    adc_value = wbit.adc()
    
    # 將數值除以240並無條件進位取商數n
    n = math.ceil(adc_value / 240)
    
    # 先全部關閉LED燈
    wbit.showAll(0, 0, 0)
    
    # 迴圈n次, 顯示第n顆LED燈為白色
    for i in range(n):
        wbit.show(i, 100, 100, 100)
    
    # 等待1秒
    wbit.sleep(1)
