from webduino.board import *

import time
from rotary_irq_esp import RotaryIRQ

time.sleep(1.5)
e01 = Board('marty')

r = RotaryIRQ(pin_num_clk=0, 
              pin_num_dt=2, 
              min_val=0, 
              max_val=17, 
              reverse=False, 
              range_mode=RotaryIRQ.RANGE_WRAP)

print('start')              
val_old = r.value()
while True:
    val_new = r.value()
    if val_old != val_new:
        val_old = val_new
        #print('result =', val_new)
        e01.mqtt.pub("www",str(val_new))
        #time.sleep_ms(100)
    time.sleep_ms(10)
