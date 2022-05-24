from webduino.board import Board
from webduino.led import LED
import time, machine

green = machine.Pin(12, machine.Pin.OUT)
blue = machine.Pin(13, machine.Pin.OUT)
red = machine.Pin(15, machine.Pin.OUT)
green.off()
blue.off()
red.on()
#####################
try:
    import cmd
    machine.reset()
except:
    pass
#####################

def cb(cmd):
    #eval(cmd)
    print(">> "+cmd)

def cb2(topic,msg):
    print(topic," , ",msg)


try:
    board = Board(devId='smart')
    # topicName = "${devId}/" + ${name}
    board.onTopic("test",cb)
    red.off()
    green.on()
    board.mqtt.sub("testok",cb2)
    board.loop()
    #board.check()
except Exception as e:
    print(e)
    print('')
    machine.reset()
