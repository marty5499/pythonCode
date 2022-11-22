import dht,time
from machine import Pin
from webduino.board import Board

sensor = dht.DHT22(Pin(2))

def measure():
    sensor.measure()
    return str(sensor.temperature())+" "+str(sensor.humidity())

try:
    print("==")
    print("-=-=-=-= base =-=-=-=-")
    print("==")
    board = Board(devId='dht22')
    while True:
        time.sleep(3)
        board.publish("sroom/data", measure())
        board.check()
except Exception as e:
    print(e)
    print('')
    machine.reset()
