from webduino.webbitv1 import WebBit
from webduino.image import get_image
wbit = WebBit()
while True:
    # 偵測按鈕狀態
    if wbit.btnA() and wbit.btnB():  # 同時按下AB
        wbit.matrix(0, 0, 100, get_image("circle"))  # 顯示藍色圓形
    elif wbit.btnA():  # 只按下A
        wbit.matrix(100, 0, 0, get_image("arrow_left"))  # 顯示紅色左三角形
    elif wbit.btnB():  # 只按下B
        wbit.matrix(0, 100, 0, get_image("arrow_right"))  # 顯示綠色右三角形
