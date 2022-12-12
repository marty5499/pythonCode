###### tags: `micropython`
ESP32s2 micropython
====

## 一、建置本機目錄

```console=
mmdir ~/esp32-mpy
cd ~/esp32-mpy

# 先clone micropython repo
git clone https://github.com/micropython/micropython.git

# 透過 docker 使用 esp-idf 環境，將 ~/esp32-mpy 目錄掛到 /project 目錄
docker run --rm -v $PWD:/project -w /project -it espressif/idf:release-v4.3
```

## 二、編譯韌體
```console=
cd ~/esp32-mpy

# 使用 docker 進入編譯環境
docker run --rm -v $PWD:/project -w /project -it espressif/idf:release-v4.3

#進入docker後，先進入 micropython 建置 cross
cd micropython
make -C mpy-cross

#編譯 esp32-s2
cd ports/esp32
make submodules
make BOARD=GENERIC_S2
```

### WebBit v2 (esp32s2) 開啟 PSRAM

修改 ports\esp32\boards\GENERIC_S2\mpconfigboard.cmake 檔案
加入一行，然後重新編譯就可以有2MBytes空間
```console=
set(IDF_TARGET esp32s2)

set(SDKCONFIG_DEFAULTS
    boards/sdkconfig.base
    boards/sdkconfig.usb
    boards/sdkconfig.spiram_sx ## add this line
)

if(NOT MICROPY_FROZEN_MANIFEST)
    set(MICROPY_FROZEN_MANIFEST ${MICROPY_PORT_DIR}/boards/manifest.py)
endif()
```





:::danger
燒錄不在容器內，並且需使用conda切換運行環境
```
> conda activate esp32
```
:::

## 三、燒錄韌體

```console=
## 進入產生韌體的目錄
cd ~/esp32-mpy/micropython/ports/esp32/build-GENERIC_S2

## erase flash
esptool.py -p /dev/cu.usbmodem01 --chip esp32s2 erase_flash

## 燒錄韌體
esptool.py --before default_reset --after hard_reset --chip esp32s2 -b 460800 -p /dev/cu.usbmodem01 write_flash 0x8000 partition_table/partition-table.bin 0x1000 bootloader/bootloader.bin 0x10000 micropython.bin

esptool.py -p /dev/cu.usbmodem01 -b 460800 --before default_reset --after hard_reset --chip esp32s2  write_flash --flash_mode dio --flash_size detect --flash_freq 80m 0x1000 build-GENERIC_S2/bootloader/bootloader.bin 0x8000 build-GENERIC_S2/partition_table/partition-table.bin 0x10000 build-GENERIC_S2/micropython.bin

```
## 四、線上燒錄
https://marty5499.github.io/bitv2/index.html
![](/uploads/upload_7e2cf325b03c39b074735fad1138373f.png =50%x)


記憶體
```console
>>> micropython.mem_info()
stack: 736 out of 15360
GC: total: 2049088, used: 9888, free: 2039200
No. of 1-blocks: 207, 2-blocks: 30, max blk sz: 24, max free sz: 127437
 ```