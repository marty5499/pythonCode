Micropython 規劃
========

# 1. 燒錄

## Micropython-espnow ESP8266 版本
![](/uploads/upload_72681320833f730c853054473a231a44.png =30%x) ![](/uploads/upload_baa85a2a127328fb6ec6e67e6336cc7b.png =30%x)![](/uploads/upload_b21739c1dbfff862122b3ba457c9dcc3.png =30%x)


### - ESP8266 : ESP01、Smart、WeMos


```console=
# 切到 esp 環境
conda acticate esp

# erase firmware 
esptool.py --port /dev/cu.wchusbserial110 --baud 460800 erase_flash

# 進到 esp8266/build-GENERIC_1M 目錄
cd /Users/sheuyih-shiang/kingkit.codes/mpy/micropython-espnow/ports/esp8266/build-GENERIC_1M

# 進行燒錄
esptool.py --port /dev/cu.wchusbserial110 --baud 460800 write_flash --flash_size=detect -fm dout 0 firmware.elf-0x00000.bin 0x09000 firmware.elf-0x09000.bin
```

更新完用 Thonny IDE 打開 v1.19.1-espnow 版本
![](/uploads/upload_44cb859c4e90fa74ec4a544a7a50e041.png)


# 2. 安裝 Webduino Lib

打開 $mpy/pythonCode/init/inst_lib_esp8266.py 執行

![](/uploads/upload_ef817c2352f858407484e09127710052.png =70%x)


# 3. 測試 main.py

訂閱 sroom/data Topic , 收到訊息執行 cb(cmd)
PS. 訂閱只能是 devId/topicName

## [參考資料交換](https://md.kingkit.codes/7oJFE2MSRYWG1b0GQjijeA)
```python=
import machine
from webduino.board import Board

def cb(cmd):
    print(">> "+cmd)

try:
    board = Board(devId='sroom')
    board.onTopic("data",cb)
    board.loop()
except Exception as e:
    print(e)
    machine.reset()
```

