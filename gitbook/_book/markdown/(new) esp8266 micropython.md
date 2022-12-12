(new) esp8266 micropython
=====

###### tags: `micropython`



## Micropython-espnow ESP01 版本
![](/uploads/upload_48da3542a70f757a17543d022bb6c201.png =30%x)


## Micropython-espnow ESP8266 版本
![](/uploads/upload_72681320833f730c853054473a231a44.png =30%x) ![](/uploads/upload_baa85a2a127328fb6ec6e67e6336cc7b.png =30%x)



## 編譯 esp8266 韌體 (micropython、micropython-espnow)：

先拉 sdk 下來
```
docker pull larsks/esp-open-sdk
```

在 [micropython](https://github.com/micropython/micropython) 或 [micropython-espnow](https://github.com/glenn20/micropython-espnow-images) 目錄下
```
cd ${micropython}

# mpy Python 編譯器：
docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make -C mpy-cross

# 建置 ESP8266 的子模組：
docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make -C ports/esp8266 submodules

# 建置 MicroPython 韌體 (選擇開發板Flash)：
cd ports/esp8266
docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make BOARD=GENERIC_1M

```

建置完成會在 ports/esp8266/build-GENERIC-????/ 下 firmware-combined.bin 檔：

```
...
LINK build-GENERIC/firmware.elf
   text	   data	    bss	    dec	    hex	filename
 586680	   1020	  66376	 654076	  9fafc	build-GENERIC/firmware.elf
Create build-GENERIC/firmware-combined.bin
esptool.py v1.2
flash     32960
padding   3904
irom0text 554776
total     591640
md5       2c449d5b010f731ebab35447bd35f9f4
```

## 燒錄韌體
```
cd build-GENERIC/

# 清除flash
esptool.py --port /dev/cu.usbserial-1440 --baud 460800 erase_flash

# LiliGo
esptool.py --port /dev/cu.wchusbserial1440 --baud 460800 erase_flash



# 燒錄
esptool.py --port /dev/cu.usbserial-1440 --baud 460800 write_flash --flash_size=detect -fm dout 0 firmware.elf-0x00000.bin 0x09000 firmware.elf-0x09000.bin

# Lily Go
esptool.py --port /dev/cu.wchusbserial1440 --baud 460800 write_flash --flash_size=detect -fm dout 0 firmware.elf-0x00000.bin 0x09000 firmware.elf-0x09000.bin

```


### ESP01 記憶體
```
>>> micropython.mem_info()
stack: 2096 out of 8192
GC: total: 37952, used: 1328, free: 36624
No. of 1-blocks: 24, 2-blocks: 13, max blk sz: 8, max free sz: 2052
 ```
```
>>> micropython.mem_info()
stack: 2160 out of 8192
GC: total: 37952, used: 5136, free: 32816
No. of 1-blocks: 109, 2-blocks: 18, max blk sz: 20, max free sz: 1916
 ```
 
 


