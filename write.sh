#!/bin/bash

#讓使用者選擇燒錄的設備

echo "Select the device to flash:"
echo "[1] ESP8266"
echo "[2] ESP01"
read -p "Enter choice (1 or 2): " device_choice

#列出所有 /dev/cu.usb\ *端口，不包括 /dev/cu.usbmodem*

echo "Available serial ports:"
ports=($(ls /dev/cu.usb* | grep -v 'cu.usbmodem'))

if [ ${#ports[@]} -eq 0 ]; then
echo "No available serial ports found. Exiting."
exit 1
elif [ ${#ports[@]} -eq 1 ]; then
port="${ports[0]}"
echo "Using port: $port"
else
for i in "${!ports[@]}"; do
echo "[$i] ${ports[$i]}"
done

#讀取使用者選擇

read -p "Select a port (number or 'd' for default): " choice

#設置選擇的端口

port="${ports[$choice]}"
echo "Using port: $port"
fi

#顯示晶片資訊

esptool.py --port $port --baud 460800 flash_id

#擦除閃存

esptool.py --port $port --baud 460800 erase_flash

#切換到 ESP8266 工作目錄

if [ "$device_choice" -eq 1 ]; then

#ESP8266 燒錄指令

esptool.py --port $port --baud 460800 write_flash --flash_size=4MB 0x00000 ./esp8266/build-ESP8266_GENERIC/firmware.elf-0x00000.bin 0x09000 ./esp8266/build-ESP8266_GENERIC/firmware.elf-0x09000.bin

#寫入文件系統備份

esptool.py --port $port --baud 460800 write_flash 0x100000 ./esp8266/filesystem_backup.bin

elif [ "$device_choice" -eq 2 ]; then

#ESP01 燒錄指令

esptool.py --port $port --baud 460800 write_flash --flash_size=detect -fm dout 0 ./esp8266/esp01_v1.23.bin
else
echo "Invalid choice. Exiting."
exit 1
fi

echo "Flashing complete."
