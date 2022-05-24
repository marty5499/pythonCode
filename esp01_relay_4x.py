from webduino.board import Board
from webduino.debug import debug
import time, machine
from machine import UART
import time

r1_on =   b'\xA0\x01\x01\xA2'
r1_off =  b'\xA0\x01\x00\xA1'
r2_on =   b'\xA0\x02\x01\xA3'
r2_off =  b'\xA0\x02\x00\xA2'
r3_on =   b'\xA0\x03\x01\xA4'
r3_off =  b'\xA0\x03\x00\xA3'
r4_on =   b'\xA0\x04\x01\xA5'
r4_off =  b'\xA0\x04\x00\xA4'

debug.off()

uart = UART(0, 115200)
uart.init(115200, bits=8, parity=None, stop=1)


#####################
try:
    import cmd
    machine.reset()
except:
    pass
#####################

def cb(cmd):
    if cmd == 'r1 on':
        uart.write(r1_on)
    elif cmd == 'r1 off':
        uart.write(r1_off)

try:
    board = Board(devId='smart')
    # topicName = "${devId}/" + ${name}
    board.onTopic("testqq",cb)
    board.loop()
    #board.check()
except Exception as e:
    print(e)
    print('')
    machine.reset()


