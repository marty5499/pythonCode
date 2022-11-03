import camera
import machine
from webduino.board import Board
from webduino.webstream import webstream

def initCamera():
    try:
        camera.init(0, format=camera.JPEG)
        camera.quality(15)
        camera.framesize(camera.FRAME_HD) # FRAME_VGA, FRAME_SVGA, FRAME_HD, FRAME_SXGA, FRAME_UXGA
    except:
        machine.reset()    

def cb(cmd):
    print(">> "+cmd)

try:
    initCamera()
    board = Board(devId='smart')
    webstream.start(camera)
    board.onTopic("test",cb)
    print("start webStream...")
    board.loop()
except Exception as e:
    print(e)
    machine.reset()
