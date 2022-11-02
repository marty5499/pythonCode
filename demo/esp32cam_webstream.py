import camera
import time
import esp
import machine
import gc
from machine import Pin
from lib.webcam.Wifi.Sta import Sta
from lib.webcam.webstream import webstream
 
esp.osdebug(True)

try:
    camera.init(0, format=camera.JPEG)
    camera.quality(15)
    camera.framesize(camera.FRAME_HD) # FRAME_VGA, FRAME_SVGA, FRAME_HD, FRAME_SXGA, FRAME_UXGA
except:
    machine.reset()

w = Sta()
w.connect()
w.wait()

print("start webStream...")
webstream.start(camera)
print("go for it...")

