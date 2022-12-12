import machine
from webduino.board import Board
from machine import Pin
from mfrc522 import MFRC522
import time

#(sck, mosi, miso, rst, cs):
rfid = MFRC522(0, 2, 4, 15,5)
led = Pin(2, Pin.OUT)

def checkRFID():
    led.value(0)  # 搜尋卡片之前先關閉 LED
    stat, tag_type = rfid.request(rfid.REQIDL)  # 搜尋 RFID 卡片
    if stat == rfid.OK:  # 找到卡片
        stat, raw_uid = rfid.anticoll()  # 讀取 RFID 卡號
        if stat == rfid.OK:
            led.value(1)  # 讀到卡號後點亮 LED
            # 將卡號由 2 進位格式轉換為 16 進位的字串
            id = "%02X%02X%02X%02X" % (raw_uid[0], raw_uid[1],
                                       raw_uid[2], raw_uid[3])
            board.publish('rfid/scan',id)
            print("偵測到卡號：", id)
            time.sleep(0.5)  # 暫停一下, 避免 LED 太快熄滅看不到




def cb(cmd):
    print(">> "+cmd)

try:
    board = Board(devId='rfid')
    board.onTopic("exec",cb)
    cnt = 0
    while True:
        cnt = cnt + 1
        checkRFID()
        if(cnt==100):
            cnt = 0
            board.check()
except Exception as e:
    print(e)
    machine.reset()