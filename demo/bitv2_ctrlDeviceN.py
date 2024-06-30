from webduino.webbit import WebBit
import ubinascii, time

class CtrlDevice_8:
    
    def __init__(self, ssid, device_id, ports):
        self.ssid = ssid
        self.device_id = device_id
        self.ports = ports
        self.msg_idx = 0
        self.wbit = WebBit()
        self.wbit.mqttServer = 'mqtt-agri.webduino.io'
    
    def get_initial_port_states(self):
        self.wbit.board.config.load()
        self.state_str = self.wbit.board.config.get('ports')
        if self.state_str is None:
            return [0] * self.ports  # 如果未取得狀態，預設所有 port 狀態都是 0
        return list(map(int, self.state_str))

    def save_port_states(self):
        self.wbit.board.config.put('ports', ''.join(map(str, self.port_states)))
        self.wbit.board.config.save()
    
    def get_msg_idx(self):
        self.msg_idx += 1
        return self.msg_idx

    def update_state_report(self):
        self.state_str = ''.join(map(str, self.port_states))
        state_report = f"{self.ssid} {''.join(reversed(self.state_str))},0,0,{self.ports},0,info,M207,{self.get_msg_idx()}"
        self.publish('_channel_', state_report)
        self.save_port_states()  # 儲存狀態

    def connect(self, qos=1):
        self.qos = qos
        self.wbit.connect()
        self.port_states = self.get_initial_port_states()
        print(f"{self.device_id}/STATUS")
        self.wbit._sub_(f"{self.device_id}/PING", self.handle_message)
        self.publish(f"{self.device_id}/STATUS", "OK")
        self.wbit.board.start()
        print("Connected to MQTT server...OK")
    
    def publish(self, topic, message):
        self.wbit._pub_(topic, message)
        print(f"out --> {message}")
    
    def turn_on(self, port):
        self.port_states[port] = 1  # 更新對應的 port 狀態
        self.wbit.showAll(100, 0, 0)
        self.update_state_report()
    
    def turn_off(self, port):
        self.port_states[port] = 0  # 更新對應的 port 狀態
        self.wbit.showAll(0, 100, 0)
        self.update_state_report()
    
    def handle_message(self, topic, message):
        topic = topic.decode('utf-8')
        print(f"in <-- {topic}")
        print("RAW:", message)
        str_msg = ''.join(chr(b) if 32 <= b <= 126 else '?' for b in message)
        print("STR:", str_msg)
        
        if topic == f"{self.device_id}/PING":
            if message == b'\xf0\x04\x10\x03controller=' + self.device_id.encode() + b'\xf7':
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x03\xf7')
                print(f"memo: controller={self.device_id}")

            elif message[:7] == b'\xf0\x04\x10\x03on=':
                port = int(chr(message[7]))  # 獲取 port 編號
                print(f'port on {port}')
                self.turn_on(port-1)
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x03\xf7')

            elif message[:8] == b'\xf0\x04\x10\x03off=':
                port = int(chr(message[8]))  # 獲取 port 編號
                print(f'port off {port}')
                self.turn_off(port-1)
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x03\xf7')

            elif message == b'\xf0\x04\x10\x03mutex=true\xf7':
                self.enable_mutex()
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x03\xf7')

            elif message == b'\xf0\x04\x10\x03unmutex=true\xf7':
                self.disable_mutex()
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x03\xf7')

            # firmataVersion
            elif message == b'\xf0\x04\x10\x02\x05\x00\xf7':
                self.publish(f"{self.device_id}/PONG", (b'\xf9\x02\x05\xf0\x79\x02\x05\x53\x00\x61\x00'
                            b'\x6e\x00\x64\x00\x61\x00\x72\x00\x64\x00'
                            b'\x46\x00\x69\x00\x72\x00\x6d\x00\x61\x00'
                            b'\x74\x00\x61\x00\x2e\x00\x69\x00\x6e\x00'
                            b'\x6f\x00\xf7'))
                self.update_state_report()
                print("memo: arduino version(1)")

            # firmataVersion
            elif message == b'\xf0\x04\x10\x05\xf7':
                self.publish(f"{self.device_id}/PONG", (b'\xf9\x02\x05\xf0\x79\x02\x05\x53\x00\x61\x00'
                            b'\x6e\x00\x64\x00\x61\x00\x72\x00\x64\x00'
                            b'\x46\x00\x69\x00\x72\x00\x6d\x00\x61\x00'
                            b'\x74\x00\x61\x00\x2e\x00\x69\x00\x6e\x00'
                            b'\x6f\x00\xf7'))
                print("memo: arduino version(2)")

            else:
                print("No matching control command, not publishing.")
            
    def enable_mutex(self):
        print("Mutex enabled")
        # 實現啟用互斥功能

    def disable_mutex(self):
        print("Mutex disabled")
        # 實現禁用互斥功能

    def save_report_interval(self, minutes, seconds):
        print(f"Saving report interval: {minutes} minutes, {seconds} seconds")
        # 實現儲存報告間隔到設備

# 使用範例 
ctrl = CtrlDevice_8("ta5589", "ePkrgmQm", 6)
ctrl.connect()

while True:
    if ctrl.wbit.btnA():
        ctrl.turn_on(0)
        time.sleep(1)
    if ctrl.wbit.btnB():
        ctrl.turn_off(0)
        time.sleep(1)