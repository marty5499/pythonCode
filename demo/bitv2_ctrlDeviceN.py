# 韌體 lib 需更新 board.py , image.py , mqtt.py , webbit.py , hs300.py
from webduino.webbit import WebBit
from webduino.debug import debug
from hs300 import HS300
import ubinascii, time

class CtrlDevice_8:
    
    def __init__(self, ssid, device_id, ports):
        #debug.on()
        self.ssid = ssid
        self.device_id = device_id
        self.ports = ports
        self.msg_idx = 0
        self.wbit = WebBit()
        self.wbit.mqttServer = 'mqtt-agri.webduino.io'
        self.wbit.topic_report = f"{self.device_id}/STATUS"
        self.wbit.topic_report_msg = ""
    
    def init_port_states(self):
        # 如果未取得狀態，預設所有 port 狀態都是 0
        self.state_str = self.load_config('ports',[0] * self.ports)
        return list(map(int, self.state_str))

    def init_plugs_port(self):
        self.hs300 = HS300(self.plugs_ip)
        # 遍歷 self.state_str 並呼叫 set_smart_plugs
        self.hs300.connect()
        for index, state in enumerate(reversed(self.state_str)):
            if(index > self.ports): break
            print(f'hs300 ip[{self.plugs_ip}],switch {index + 1} state:{state}')
            success = self.hs300.sw(index, int(state))
        self.hs300.close()

    def load_config(self,key, defValue=''):
        self.wbit.board.config.load()
        val = self.wbit.board.config.get(key)
        if(val == None):
            val = defValue
        return val

    def save_config(self,key,value):
        self.wbit.board.config.put(key, value)
        self.wbit.board.config.save()

    def save_port_states(self):
        self.save_config('ports', ''.join(map(str, self.port_states)))
    
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
        self.cronSec = int(self.load_config('cronSec','30'))
        self.port_states = self.init_port_states()
        self.plugs_ip = self.load_config('plugs','192.168.0.4')
        self.init_plugs_port()
        print(f'set plugs_ip: {self.plugs_ip}')
        print(f"{self.device_id}/STATUS")
        self.wbit._sub_(f"{self.device_id}/PING", self.handle_message)
        self.publish(f"{self.device_id}/STATUS", "OK")
        self.wbit.board.start()
        print("Connected to MQTT server...OK")
    
    def publish(self, topic, message):
        self.wbit._pub_(topic, message)
        print(f"out --> {message}")

    def set_smart_plugs(self, port, state):
        print(f'hs300 ip[{self.plugs_ip}],switch {port} state:{state}')
        self.hs300 = HS300(self.plugs_ip)
        self.hs300.connect()
        success = self.hs300.sw(port, state)
        self.hs300.close()
    
    def turn_on(self, port):
        self.port_states[port] = 1  # 更新對應的 port 狀態
        self.set_smart_plugs(port,1)
        self.wbit.matrix(0,200,0,str(port+1))
        self.update_state_report()
    
    def turn_off(self, port):
        self.port_states[port] = 0  # 更新對應的 port 狀態
        self.set_smart_plugs(port,0)
        self.wbit.matrix(200,0,0,str(port+1))
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

            # cronTime=10 sec ~ 300 sec
            elif message[:4] == b'\xf0\x04\x10\x02':
                high_byte = message[4]
                low_byte = message[5]
                self.cronSec = high_byte * 60 + low_byte
                print(f'cronSec {self.cronSec}')
                self.save_config("cronSec",str(self.cronSec))
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x02\xf7')

            # on=?
            elif message[:7] == b'\xf0\x04\x10\x03on=':
                port = int(chr(message[7]))  # 獲取 port 編號
                print(f'port on {port}')
                self.turn_on(port-1)
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x03\xf7')

            # off=?
            elif message[:8] == b'\xf0\x04\x10\x03off=':
                port = int(chr(message[8]))  # 獲取 port 編號
                print(f'port off {port}')
                self.turn_off(port-1)
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x03\xf7')

            # list=true 行程控制 （尚未實作)
            elif message == b'\xf0\x04\x10\x03list=true\xf7':
                print(f'list=true 行程控制 （尚未實作)')
                #self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x03\xf7')

            # mutex=true
            elif message == b'\xf0\x04\x10\x03mutex=true\xf7':
                self.enable_mutex()
                self.publish(f"{self.device_id}/PONG", b'\xf0\x04\x10\x03\xf7')

            # unmutex=true
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


# 使用範例 
cntSec = 0
ctrl = CtrlDevice_8("ta5589", "ePkrgmQm", 6)
ctrl.connect()

while True:
    time.sleep(0.1)
    cntSec += 0.1
    if(int(cntSec) >= ctrl.cronSec):
        print(f'trigger...{int(cntSec)}')
        ctrl.update_state_report()
        cntSec = 0
    if ctrl.wbit.btnA():
        ctrl.turn_on(0)
    if ctrl.wbit.btnB():
        ctrl.turn_off(0)