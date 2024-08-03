# 設定使用 micropython repo建議版本
cd /opt/esp/idf
git checkout v5.0.4
git submodule update --init --recursive
./install.sh
. ./export.sh


cd /project/micropython
make -C mpy-cross

# rebuild need to make submodules
cd /project/micropython/ports/esp32
rm -rf /project/micropython/ports/esp32/build-ESP32_GENERIC_S3
make clean
make submodules
#make
make BOARD=ESP32_GENERIC_S3
