from webduino.board import Board
import machine, time

try:
    time.sleep(1.5)
    board = Board(devId='c01')
    board.start(checkTime=0.25)

    # mqtt sub
    def runCode(msg):
        try:
            exec(msg)
        except:
            machine.reset()

    board.onTopic('app',runCode)

except Exception as e:
    print(e)
    machine.reset()