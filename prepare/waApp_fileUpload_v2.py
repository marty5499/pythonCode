from webduino.board import Board
from webduino.led import LED
from webduino.camera import Camera
from webduino.filebrowser import FileBrowser
import ntptime,time, machine, gc, os


try:
    
    print("-=-=-=-= base =-=-=-=-")
    board = Board(devId='0912')
    print("cam init...")
    led = LED(4)
    led.blink(0.25)
    Camera.init()
    led.blink(0)
    gc.collect()
    print("fileUpload...")
    resp = FileBrowser.upload(Camera.capture(),'zz.jpg')
    print("body:%s"%resp[1])

except Exception as e:
    
    print(e)
    print('')
    machine.reset()
