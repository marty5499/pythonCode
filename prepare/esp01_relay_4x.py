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

debug.on()
debug.off()

r1 = False
r2 = False
r3 = False
r4 = False
uart = UART(0, 115200)
uart.init(115200, bits=8, parity=None, stop=1)


#####################
try:
    import cmd
    machine.reset()
except:
    pass
#####################

def update():
    global r1,r2,r3,r4
    data = str(r1)+' '+str(r2)+' '+str(r3)+' '+str(r4)
    board.pub('smart/state',data)
    

def cb(cmd):
    global r1,r2,r3,r4
    if cmd == 'state':
        update()
        
    elif cmd == 'r1 on':
        uart.write(r1_on)
        r1 = True
        update()
    elif cmd == 'r1 off':
        uart.write(r1_off)
        r1 = False
        update()
        
    elif cmd == 'r2 on':
        uart.write(r2_on)
        r2 = True
        update()
    elif cmd == 'r2 off':
        uart.write(r2_off)
        r2 = False
        update()
        
    elif cmd == 'r3 on':
        uart.write(r3_on)
        r3 = True
        update()
    elif cmd == 'r3 off':
        uart.write(r3_off)
        r3 = False
        update()
        
    elif cmd == 'r4 on':
        uart.write(r4_on)
        r4 = True
        update()
    elif cmd == 'r4 off':
        uart.write(r4_off)
        r4 = False
        update()

try:
    board = Board(devId='smart')
    # topicName = "${devId}/" + ${name}
    board.onTopic("4xRelay",cb)
    board.loop()
    #board.check()
except Exception as e:
    print(e)
    print('')
    machine.reset()