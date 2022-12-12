from webduino.board import Board
import time,machine

from machine import Pin
p2 = Pin(2, Pin.OUT)

def cb(cmd):
    if(cmd=='0'):
        p2.value(0)
    if(cmd=='1'):
        p2.value(1)

try:
    p2.value(0)
    time.sleep(0.5)
    p2.value(1)
    board = Board()
    board.onTopic("led",cb)
    p2.value(0)
    board.loop()
except Exception as e:
    print(e)
    machine.reset()