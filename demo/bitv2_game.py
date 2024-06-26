import time
from webduino.webbit import WebBit
from webduino.image import get_image
wbit = WebBit()
dice_value = 1  # 初始化骰子數值為1
while True:
    # 顯示對應的骰子圖形
    if dice_value == 1:
        wbit.matrix(100, 100, 100, get_image("one"))
    elif dice_value == 2:
        wbit.matrix(100, 100, 100, get_image("two"))
    elif dice_value == 3:
        wbit.matrix(100, 100, 100, get_image("three"))
    elif dice_value == 4:
        wbit.matrix(100, 100, 100, get_image("four"))
    elif dice_value == 5:
        wbit.matrix(100, 100, 100, get_image("five"))
    elif dice_value == 6:
        wbit.matrix(100, 100, 100, get_image("six"))
    time.sleep(0.25)  # 延遲0.25秒
    # 檢查按鈕A是否按下
    if wbit.btnA():
        # 如果按下按鈕A
        if dice_value == 6:
            # 如果骰子數值為6，顯示綠色笑臉
            wbit.matrix(0, 100, 0, get_image("happy"))
        else:
            # 如果骰子數值不為6，顯示紅色哭臉
            wbit.matrix(100, 0, 0, get_image("cry"))
        time.sleep(2)  # 延遲2秒
        dice_value = 1  # 重新初始化骰子數值為1
    else:
        # 如果沒按下按鈕A
        dice_value += 1  # 增加骰子數值
        if dice_value > 6:
            # 如果骰子數值大於6，將骰子數值設為1
            dice_value = 1
