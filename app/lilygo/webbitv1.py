
import time
from webduino.webbitv1 import WebBit
from webduino.image import get_image

wbit = WebBit()


while True:
    # 偵測按鈕狀態
    if wbit.btnA():  # 只按下A
      wbit.matrix(0, 100, 0, get_image("arrow_right"))  # 顯示綠色右三角形Ω
      esp.send('^_^,AA')
    if wbit.btnB():  # 只按下B
      wbit.matrix(100, 0, 0, get_image("arrow_left"))  # 顯示紅色左三角形
      esp.send('Q_Q,BB')





