###### tags: `micropython`
esp32-c3
====

https://cnx-software.cn/2021/07/19/esp32-c3-board-battery-holder/
![](/uploads/upload_1a9a4eae2cf94a2179a2f53343331ff5.png)



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

# 更新cmake , 移除原有cmake： 
apt remove cmake

# 安装新cmake：
cd ~

# 下载cmake
wget https://cmake.org/files/v3.12/cmake-3.12.2-Linux-x86_64.tar.gz
# 解压：
tar zxvf cmake-3.12.2-Linux-x86_64.tar.gz
# 创建软链接
# 注: 文件路径是可以指定的, 一般选择在/opt 或 /usr 路径下, 这里选择/opt
mv cmake-3.12.2-Linux-x86_64 /opt/cmake-3.12.2
ln -sf /opt/cmake-3.12.2/bin/*  /usr/bin/
然后执行命令检查一下：

>>>cmake --version
cmake version 3.12.2
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
# https://www.i4k.xyz/article/qq_34440409/119175631
  更改ports/esp32/Makefile文件
  到 BOARD ?= GENERIC 改为 BOARD ?= GENERIC_C3
cd ports/esp32
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
## 進入產生韌體的目錄
cd ~/esp32-mpy/micropython/ports/esp32/build-GENERIC_S2

## erase flash
esptool.py -p /dev/cu.wchusbserial1440 --chip esp32c3 erase_flash

## 燒錄韌體
esptool.py --before default_reset --after hard_reset --chip esp32c3 -b 460800 -p /dev/cu.wchusbserial1440 write_flash 0x8000 partition_table/partition-table.bin 0x1000 bootloader/bootloader.bin 0x10000 micropython.bin

```
