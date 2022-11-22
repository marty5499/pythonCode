import camera
import machine
from webduino.board import Board
from webduino.webstream import webstream

def cb(cmd):
    print(">> "+cmd)

try:
    camera.init(0, format=camera.JPEG)
    camera.quality(12)
    # FRAME_VGA, FRAME_SVGA 1024x768, FRAME_HD 1280x720, FRAME_SXGA, FRAME_UXGA
    camera.framesize(camera.FRAME_VGA)
    # connect wifi
    board = Board(devId='esp32cam')
    board.onTopic("test",cb) # subscribe: esp32cam/test
    # start stream
    webstream.start(camera)
    print("start webStream port:8080 ...")
    board.loop()
except Exception as e:
    print(e)
    machine.reset()
