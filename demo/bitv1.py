from webduino.webbitv1 import WebBit  
import time

wbit = WebBit()
# 點亮
wbit.setPin(0,True)
time.sleep(1)
# 熄滅
wbit.setPin(0,False)

