import time
from webduino.webbitv1 import WebBit
# 初始化 WebBit 物件
wbit = WebBit()
# 設定顏色列表
colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (128, 0, 128)]
# 設定亮度列表
brightness_levels = [5, 10, 15, 20, 25]
current_time = 100
val = 1
# 無限迴圈
while True:
    # 獲取當前時間
    current_time += val
    # 計算每顆燈的顏色和亮度
    for row in range(5):
        for col in range(5):
            # 計算燈的顏色索引
            color_index = int((row + col + current_time) % len(colors))
            color = colors[color_index]
            # 計算燈的亮度
            brightness = brightness_levels[row]
            # 顯示燈效果
            wbit.show(row * 5 + col, color[0] * brightness // 100, color[1] * brightness // 100, color[2] * brightness // 100)
    # 檢查速度控制
    if wbit.btnA():
        delay = 0.01  # 按下按鈕A，減慢速度
        val = -1
    elif wbit.btnB():
        delay = 0.01  # 按下按鈕B，加快速度
        val = 1
    else:
        delay = 0.1  # 預設延遲時間
    # 調整延遲時間
    time.sleep(delay)

