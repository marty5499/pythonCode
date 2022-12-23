from machine import PWM, Pin
import time

def angle(du):
    t1 = 0.5 + 2 / 180 * du
    return int(t1 / 20 * 1024)

pwm = PWM (Pin(0), freq=50,  duty=0)


for i in range(0,180):
    pwm.duty(angle(i))
    print("angle:%d",i)
    time.sleep(0.025)
print('done')

pwm.deinit()
