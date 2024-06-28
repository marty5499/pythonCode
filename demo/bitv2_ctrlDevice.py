from webduino.webbit import WebBit
import ubinascii,time

class CtrlDevice:
    
    def __init__(self, ssid, device_id):
        self.ssid = ssid
        self.device_id = device_id
        self.msg_idx = 0
        self.wbit = WebBit()
        self.wbit.mqttServer = 'mqtt-agri.webduino.io'
    
    def get_msg_idx(self):
        self.msg_idx += 1
        return self.msg_idx

    def connect(self, qos=1):
        self.qos = qos
        self.wbit.connect()
        print(f"{self.device_id}/STATUS")
        self.wbit._sub_(f"{self.device_id}/PING", self.handle_message)
        self.publish(f"{self.device_id}/STATUS", "OK")
        print("Connected to MQTT server...OK")
    
    def publish(self, topic, message):
        self.wbit._pub_(topic, message)
        print(f"out --> {ubinascii.hexlify(message).decode('utf-8')}")
        
    def turn_on(self):
        self.wbit.showAll(50, 0, 0)
        state_report = f"{self.ssid} 0.000,1,0,0,info,M201,{self.get_msg_idx()}"
        print(f"out --> {state_report}")
        self.publish('_channel_', state_report)        
    
    def turn_off(self):
        self.wbit.showAll(0, 50, 0)
        state_report = f"{self.ssid} 0.000,0,0,0,info,M201,{self.get_msg_idx()}"
        print(f"out --> {state_report}")
        self.publish('_channel_', state_report)        
    
    def handle_message(self, topic, message):
        topic = topic.decode('utf-8')
        print(f"in <-- {topic}")
        # 打印進來的消息
        print("RAW:", message)
        # 將 message 轉換成 string 表示
        str_msg = ''.join(chr(b) if 32 <= b <= 126 else '?' for b in message)
        print("STR:", str_msg)
        
        if topic == f"{self.device_id}/PING":
            if message == b'\xf0\x04\x10\x03controller=' + self.device_id.encode() + b'\xf7':
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x03\xf7')
                print(f"memo: controller={self.device_id}")
            elif message == b'\xf0\x04\x10\x03on=true\xf7':
                self.turn_on()
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x03\xf7')
            elif message == b'\xf0\x04\x10\x03off=true\xf7':
                self.turn_off()
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x03\xf7')
            elif message == b'\xf0\x04\x10\x04\xf7':
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x04\xf7')
                print("memo: unknown")
            elif message == b'\xf0\x04\x10\x02\x05\x00\xf7':
                self.publish(f"{self.device_id}/PONG", (b'\xf9\x02\x05\xf0\x79\x02\x05\x53\x00\x61\x00'
                            b'\x6e\x00\x64\x00\x61\x00\x72\x00\x64\x00'
                            b'\x46\x00\x69\x00\x72\x00\x6d\x00\x61\x00'
                            b'\x74\x00\x61\x00\x2e\x00\x69\x00\x6e\x00'
                            b'\x6f\x00\xf7'))
                print("memo: arduino version(1)")
            elif message == b'\xf0\x04\x10\x05\xf7':
                self.publish(f"{self.device_id}/PONG", (b'\xf9\x02\x05\xf0\x79\x02\x05\x53\x00\x61\x00'
                            b'\x6e\x00\x64\x00\x61\x00\x72\x00\x64\x00'
                            b'\x46\x00\x69\x00\x72\x00\x6d\x00\x61\x00'
                            b'\x74\x00\x61\x00\x2e\x00\x69\x00\x6e\x00'
                            b'\x6f\x00\xf7'))
                print("memo: arduino version(2)")
            elif message == b'\xf0\x04\x10\x03refresh=true\xf7':
                print('對應的字串為 "refresh=true"')
                # 自定義處理 refresh=true 消息
            elif (len(message) == 7 and message[0] == 0xf0 and
                  message[1] == 0x04 and message[2] == 0x10 and
                  message[3] == 0x02 and message[6] == 0xf7):
                mm = message[4]
                ss = message[5]
                print(f"Set report interval to {mm} minutes and {ss} seconds")
                self.save_report_interval(mm, ss)
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x02\xf7')
            else:
                print("No matching control command, not publishing.")
                return
            

    def save_report_interval(self, minutes, seconds):
        print(f"Saving report interval: {minutes} minutes, {seconds} seconds")
        # 實現儲存報告間隔到設備

# 使用範例 
ctrl = CtrlDevice("ta5589", "ePkrgmQm")
ctrl.connect()
print("connect OK")
ctrl.wbit.board.start()

while True:
    if ctrl.wbit.btnA():
        ctrl.turn_on()
        time.sleep(1)
    if ctrl.wbit.btnB():
        ctrl.turn_off()
        time.sleep(1)