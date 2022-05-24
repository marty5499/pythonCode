from webduino.board import Board

def cb(cmd):
    print(">> "+cmd)

try:
    board = Board(devId='esp32')
    board.onTopic("test",cb)
    board.loop()
except Exception as e:
    print(e)
    machine.reset()