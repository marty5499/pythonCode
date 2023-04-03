from webbit import WebBit
import utime

def on_message(topic, message):
    print(">>>>"+topic)
    if topic == 'bitv2/test':
        # 控制LED顯示為綠色
        wbit.showAll(0, 55, 55)

# 初始化WebBit實例
wbit = WebBit()
wbit.connect()

# 設置MQTT回調方法
wbit.sub('bitv2/test', on_message)

while True:
    # 檢查是否有收到MQTT訊息
    wbit.checkMsg()
    # 等待1秒鐘
    utime.sleep(1)
