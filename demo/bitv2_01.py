
import time
from webbit import WebBit

wbit = WebBit()
wbit.connect()

def on_message(topic, msg):
    if topic == 'bitv2/test':
        if msg == 'red':
            wbit.showAll(50, 0, 0)
        elif msg == 'green':
            wbit.showAll(0, 50, 0)
        elif msg == 'blue':
            wbit.showAll(0, 0, 50)

wbit.sub('bitv2/test', on_message)

while True:
    wbit.checkMsg()
    time.sleep(1)


