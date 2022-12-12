###### tags: `micropython`
Esp32Cam
====
> [[回首頁]](https://md.kingkit.codes/cYuxdDkOSJ2guIzPG-KHqA?view)
 
### 可參考 WebServer 寫法
https://github.com/shariltumin/esp32-cam-micropython-2022
 
 
![](/uploads/upload_613552a6581a20069bbb7f60dfd4aa2e.png)

### 內建一顆LED燈 GPIO33
![](/uploads/upload_ebaba600efb4e1d24ee751bf582bcdcc.png =30%x)


## MicroSD 使用腳位

|   ESP32 | Touch | ADC2 | MicroSD            |
| -------:| -----:| ---- |:------------------ |
| GPIO 12 |     o | o    | DATA2              |
| GPIO 13 |     o | o    | DATA3              |
| GPIO 15 |     o | o    | CMD                |
|  GPIO14 |     o | o    | CLK                |
|  GPIO02 |     o | o    | DATA0              |
|  GPIO04 |     o |      | DATA1 / flashlight |
|  GPIO16 |       |      |                    |
|   GPIO0 |     o |      |                    |
|   GPIO3 |       |      |                    |
|   GPIO1 |       |      |                    |


## 鏡頭

|   X-JM0007A 廣角鏡頭 | X-JM0008B 魚眼鏡頭 | 
| -------:| -----:| 
| ![](/uploads/upload_c9d99f62e9f5bc3fc87226496ab3d8bd.png) | ![](/uploads/upload_8a2748cbd0b43302575d945729da2548.png) | 



### 雲端更新燒錄

#### [燒錄網址](https://marty5499.github.io/waboard/esp32cam.html)

![](/uploads/upload_4323c2bcfb576ac5931525f2d674a5d0.png)


### 很多 esp32Cam 範例
https://randomnerdtutorials.com/projects-esp32-cam/

### 寫照片到檔案中
https://www.bilibili.com/read/cv8818646



## Google Script App 檔案上傳的腳本
```javascript=
// queryString 就是 e.parameters
// req: https://script.google.com/script/exec?filename=ok.jpg&folderId=asdklfn4ou83n
// res: {"id":"123456789" , "name":"ok.jpg" , "size":77656}

function doPost(e) {
 var strAux = e.parameter.data;
 var strInput = strAux.replace(/ /g, "+");
 var folderId = e.parameters.folderId;
 var decoded = Utilities.base64Decode(strInput, Utilities.Charset.UTF_8);
 var blob = Utilities.newBlob(decoded , MimeType.JPEG, e.parameters.filename);
 var file = DriveApp.getFolderById(folderId).createFile(blob);
 var fileObj = {
   'id':file.getId(),
   'name':file.getName(),
   'size':file.getSize()
 }
 return ContentService.createTextOutput(JSON.stringify(fileObj)).setMimeType(ContentService.MimeType.JSON);
}
```

## 檔案上傳的 mpy 程式碼
```python=
import network
from machine import Pin, Timer, I2C, ADC
import camera
import machine
import time
import uasyncio as asyncio
import ubinascii
import gc
import usocket
import json
import urequests

def do_connect():
    global connected
    sta_if = network.WLAN(network.STA_IF)
    if(not sta_if.isconnected()):
        sta_if.active(True)
        sta_if.connect('KingKit_2.4G', 'webduino')
        cnt = 0
        while not sta_if.isconnected():
            cnt = cnt + 1
            time.sleep(0.5)
            if cnt == 12:
                break
    print('network config:', sta_if.ifconfig())

    
def cameraInit():
    camera.init(0, format=camera.JPEG,xclk_freq=camera.XCLK_20MHz)
    camera.framesize(15)
    camera.quality(10)
    camera.framesize(camera.FRAME_XGA)
    time.sleep(0.1)
    
def snapshot():
    jpg = camera.capture()
    image = ubinascii.b2a_base64(jpg)
    del jpg
    time.sleep(0.1)
    gc.collect()
    return image
    
    
def upload(image,idx):
    myScriptID = 'AKfycbxsmXppkOGdGNftGKSXrWJcFTr8qOI5iior8KNMnNY7ebq4SO6ATKASPgMdFFINYKnNcw'
    url = 'https://script.google.com/macros/s/'+myScriptID+'/exec'
    myFilename = "filename="+str(idx)+".jpg&mimetype=image/jpeg&data="
    myDomain = "script.google.com"

    data = myFilename + image.decode()
    method = "POST"
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    elif proto == "https:":
        import ussl
        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)
    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
    ai = ai[0]
    s = usocket.socket(ai[0], ai[1], ai[2])
    s.connect(ai[-1])
    if proto == "https:":
        s = ussl.wrap_socket(s, server_hostname=host)
    s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
    s.write(b"Host: %s\r\n" % host)
    s.write(b"Content-Length: %d\r\n" % len(data))
    s.write(b"Content-Type: application/x-www-form-urlencoded\r\n")
    s.write(b"\r\n")
    s.write(data)
    # response
    l = s.readline()
    l = l.split(None, 2)
    status = int(l[1])
    reason = ""
    if len(l) > 2:
        reason = l[2].rstrip()
    while True:
        l = s.readline()
        if not l or l == b"\r\n":
            break
        if l.startswith(b"Transfer-Encoding:"):
            if b"chunked" in l:
                raise ValueError("Unsupported " + l)
    
    
print("connecting...")
do_connect()

print("init camera...")
cameraInit()

idx = 0
while True:
    idx = ++idx
    print("snapshot..."+str(idx))
    image = snapshot()
    print("upload...")
    upload(image,idx)
print("done.")
```


### ESP32-CAM 相關參數

```
import camera
#引入camera库
camera.init(0, format=camera.JPEG)  
#初始化相机


设置分辨率（不设置分辨率默认是200万像素）
camera.framesize(camera.FRAME_240X240)

分辨率参数：
camera.FRAME_96X96   96x96
camera.FRAME_240X240   240x240
camera.FRAME_QVGA    320X240
camera.FRAME_VGA   640x480
camera.FRAME_SVGA    800x600
camera.FRAME_HD     1280X720
 

设置特殊模式

# specialeffects
camera.speffect(camera.EFFECT_NONE)
# The optionsare the following:
# EFFECT_NONE(default) EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO

参数
EFFECT_NEG 偏紫色
BW 黑白
RED 红
GEEN 绿
Blue 蓝
RETRO 怀旧风格

 

#设置白平衡
# white balance
camera.whitebalance(camera.WB_NONE)
# The optionsare the following:
# WB_NONE(default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

 

#设置饱和度
# saturation
camera.saturation(0)
# -2,2 (default0). -2 grayscale

 

#设置亮度
# brightness
camera.brightness(0)
# -2,2 (default0). 2 brightness


#设置对比度
# contrast
camera.contrast(0)
#-2,2 (default0). 2 highcontrast


#设置图片质量
# quality
camera.quality(10)
# 10-63 lowernumber means higher quality
 

所有设置必须在camera.capture()执行之前。

#拍照
buf = camera.capture()
img=open("a.jpg","w")
img.write(img)
img.close()

 

#SD卡挂载
import uos
from machine import SDCard
uos.mount(SDCard(),'/sd')

#挂载在SD卡上了
uos.chdir('sd') #切换到sd卡目录
uos.listdir() #查看文件下所有的文件 作者：邪恶的胖次菌 https://www.bilibili.com/read/cv8818646 出处：bilibili
```




```
object <module 'camera'> is of type module
  __name__ -- camera
  init -- <function>
  deinit -- <function>
  capture -- <function>
  flip -- <function>
  mirror -- <function>
  framesize -- <function>
  quality -- <function>
  contrast -- <function>
  saturation -- <function>
  brightness -- <function>
  speffect -- <function>
  whitebalance -- <function>
  JPEG -- 3
  YUV422 -- 1
  GRAYSCALE -- 2
  RGB565 -- 0
  FRAME_96X96 -- 0
  FRAME_QQVGA -- 1
  FRAME_QCIF -- 2
  FRAME_HQVGA -- 3
  FRAME_240X240 -- 4
  FRAME_QVGA -- 5
  FRAME_CIF -- 6
  FRAME_HVGA -- 7
  FRAME_VGA -- 8
  FRAME_SVGA -- 9
  FRAME_XGA -- 10
  FRAME_HD -- 11
  FRAME_SXGA -- 12
  FRAME_UXGA -- 13
  FRAME_FHD -- 14
  FRAME_P_HD -- 15
  FRAME_P_3MP -- 16
  FRAME_QXGA -- 17
  FRAME_QHD -- 18
  FRAME_WQXGA -- 19
  FRAME_P_FHD -- 20
  FRAME_QSXGA -- 21
  FRAME_QSXGA -- 21
  WB_NONE -- 0
  WB_SUNNY -- 1
  WB_CLOUDY -- 2
  WB_OFFICE -- 3
  WB_HOME -- 4
  EFFECT_NONE -- 0
  EFFECT_NEG -- 1
  EFFECT_BW -- 2
  EFFECT_RED -- 3
  EFFECT_GREEN -- 4
  EFFECT_BLUE -- 5
  EFFECT_RETRO -- 6
  XCLK_10MHz -- 10000000
  XCLK_20MHz -- 20000000
  ```
