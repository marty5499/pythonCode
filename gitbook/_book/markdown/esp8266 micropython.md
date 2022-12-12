###### tags: `micropython`
esp8266 micropython
===
## Micropython-espnow ESP32 版本
![](/uploads/upload_48da3542a70f757a17543d022bb6c201.png =30%x)
### 透過 docker 提供 esp make 指令編譯 esp8266 micropython
docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make *BOARD=GENERIC_1M*

# 編譯擴充模組


## Micropython-espnow ESP01 版本
![](/uploads/upload_48da3542a70f757a17543d022bb6c201.png =30%x)
```console=

docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make clean

docker run --rm -v $HOME:$HOME  -u $UID -w $PWD larsks/esp-open-sdk make BOARD=GENERIC_1M

rm -rf build-GENERIC_1M

docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make BOARD=GENERIC_1M USER_C_MODULES=../../../modules CFLAGS_EXTRA=-DMODULE_SIMPLEFUNCTION_ENABLED=1 all

```
### Step1. make clean
alias clean="docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make clean"

### Step2. 產生韌體 esp01 韌體
alias dmake="docker run --rm -v $HOME:$HOME  -u $UID -w $PWD larsks/esp-open-sdk make BOARD=GENERIC_1M"

### Step3. 刪除輸出目錄
rm -rf build-GENERIC_1M

### Step4. 再產生自定義模組 GENERIC_1M
alias build="docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make BOARD=GENERIC_1M USER_C_MODULES=../../../modules CFLAGS_EXTRA=-DMODULE_SIMPLEFUNCTION_ENABLED=1 all"


## Micropython-espnow ESP8266 版本
![](/uploads/upload_72681320833f730c853054473a231a44.png =30%x) ![](/uploads/upload_baa85a2a127328fb6ec6e67e6336cc7b.png =30%x)


```console=

docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make clean

docker run --rm -v $HOME:$HOME  -u $UID -w $PWD larsks/esp-open-sdk make BOARD=GENERIC

rm -rf build-GENERIC

docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make BOARD=GENERIC USER_C_MODULES=../../../modules CFLAGS_EXTRA=-DMODULE_SIMPLEFUNCTION_ENABLED=1 all

```

### Step1. make clean
alias clean="docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make clean"

### Step2. 產生韌體 esp8266 韌體
alias dmake="docker run --rm -v $HOME:$HOME  -u $UID -w $PWD larsks/esp-open-sdk make BOARD=GENERIC"

### Step3. 刪除輸出目錄
rm -rf build-GENERIC

### Step4. 再產生自定義模組 GENERIC
alias build="docker run --rm -v $HOME:$HOME -u $UID -w $PWD larsks/esp-open-sdk make BOARD=GENERIC USER_C_MODULES=../../../modules CFLAGS_EXTRA=-DMODULE_SIMPLEFUNCTION_ENABLED=1 all"




## 編譯 esp8266 韌體：

先拉 sdk 下來
```
docker pull larsks/esp-open-sdk
```

在 micropython 或 micropython-espnow 目錄下
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
 
 

