import time
from webduino.webbit import WebBit

# 初始化開發板
wbit = WebBit()
wled = {0:20,1:15,2:10,3:5,4:0,5:21,6:16,7:11,8:6,9:1,10:22,11:17,12:12,13:7,14:2,15:23,16:18,17:13,18:8,19:3,20:24,21:19,22:14,23:9,24:4}

# 將顏色碼顯示在指定的燈號上
def show_color_on_led(data):
    wbit.showAll(0,0,0)
    for i in range(0, len(data), 8):
        num = int(data[i:i+2],16) # 燈號
        num = wled[num]
        hex_color = data[i+2:i+8] # 顏色
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        #if r!=0 or g!=0 or b!=0:print(data[i:i+8])
        wbit.show(num, r, g, b)

# 解析燈號與顏色資料
data = "0000000001ff000002ff000003ff0000040000000500000006ff000007ffcc0008ff0000090000000a0000000bff00000cff00000dff00000e0000000f44ff44100000001144ff44120000001343ff44140000001544ff441644ff441744ff4418000000"
# 花,小花
data = "01ff000002ff000003ff000006ff000007ffcc0008ff00000bff00000cff00000dff00000f44ff441144ff441343ff441544ff441644ff441744ff44"
show_color_on_led(data)
