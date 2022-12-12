###### tags: `micropython`
ESP32 micropython
====

## 一、建置本機目錄

- micropython 目錄就是開源程式碼的git repo
- 使用Docker進行編譯，Espressif 官方提供的 Container 

```console=
## 使用 docker 編譯 esp32 韌體 (esp-idf v4.2)
```console=
mdir ~/esp32-mpy
cd ~/esp32-mpy

# 先clone micropython repo
git clone https://github.com/micropython/micropython.git

# 使用 esp-idf 環境，掛入當下 micropython 目錄
docker run --rm -v $PWD:/project -w /project -it espressif/idf:release-v4.2
```

## 二、編譯韌體
```console=
# 使用 esp-idf 環境，掛入當下 micropython 目錄
docker run --rm -v $PWD:/project -w /project -it espressif/idf:release-v4.2

#進入docker後，先進入 micropython 建置 cross
cd micropython
make -C mpy-cross

#然後進入 ports/esp32 進行編譯，輸出目錄在 build-${chip}
ports/esp32
#esp32 有 generic , s2 等型號，可以修改 Makefile 選用指定型號
#然後再進行 make 
make submodules
make

```

:::danger
燒錄不在容器內，並且需使用conda切換運行環境
```
> conda activate esp32
```
:::

## 三、燒錄韌體

```console=
# 這動作不在container 裡面，直接shell進到下面目錄
cd ~/kingkit.codes/mpy/micropython/ports/esp32/build-GENERIC

# 切換可燒錄環境
conda activate esp

# 執行燒錄程式
esptool.py -b 230400 -p /dev/cu.wchusbserial10 write_flash --flash_mode dio --flash_freq 40m --flash_size 4MB 0x8000 partition_table/partition-table.bin 0x1000 bootloader/bootloader.bin 0x10000 micropython.bin
```


