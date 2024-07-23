import time, machine, camera, ubinascii, gc

class Camera():
    
    def init():
        try:
            Camera.initState
        except:
            Camera.initState = 0
        if Camera.initState is not 1:
            try:
                #camera.init(0, format=camera.JPEG,xclk_freq=camera.XCLK_20MHz)
                #camera.init(0, format=camera.JPEG,xclk_freq=camera.XCLK_20MHz)
                camera.init(0, format=camera.JPEG)
                #camera.framesize(camera.FRAME_VGA)  #O
                #camera.framesize(camera.FRAME_SVGA) #O
                camera.framesize(camera.FRAME_XGA)  #O
                #camera.framesize(12) X
                #camera.framesize(camera.FRAME_HD) X
                #camera.framesize(camera.FRAME_UXGA) X
                #camera.framesize(camera.FRAME_HD) # 8:VGA , 10:640x480 , 12:1280x1024
                #camera.quality(10)
                #time.sleep(0.1)
                #Camera.initState = 1
            except:
                print("Camera exception !!!")
                Camera.initState = -1
                machine.reset()
                pass
 
    def snapshot():
        jpg = camera.capture()
        image = ubinascii.b2a_base64(jpg)
        del jpg
        time.sleep(0.1)
        gc.collect()
        return image

    def capture():
        gc.collect()
        return camera.capture()