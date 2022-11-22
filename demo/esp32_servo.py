from machine import Pin,PWM
import time
sg_pin32=PWM(Pin(32),freq=50,duty=0)  #front-left
sg_pin21=PWM(Pin(21),freq=50,duty=0)  #front-right
sg_pin14=PWM(Pin(14),freq=50,duty=0)  #back-left
sg_pin16=PWM(Pin(16),freq=50,duty=0)  #back-right
d_zero=(int)(1023*0.025) #0.5ms
d_30=(int)(1023*0.020) #0.5ms
d_90  =(int)(1023*0.0725) #1.45ms
d_150 =(int)(1023*0.09)  #2.4ms
d_180 =(int)(1023*0.12)  #2.4ms
#de_map=[d_90,d_zero,d_90,d_180]
de_map=[d_90,d_zero,d_90]
cnt = 0
try:
    while True:
        for i in de_map:
            sg_pin32.duty(i)
            sg_pin21.duty(i)
            sg_pin14.duty(i)
            sg_pin16.duty(i)
            time.sleep(0.25)
        cnt = cnt +1
        if cnt==10:
            break
except Exception as e:
    print(e)
    sg_pin.deinit()