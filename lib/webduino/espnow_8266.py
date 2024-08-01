import espnow, ubinascii, network
import machine, time, gc

class ESPNow:
    def __init__(self):
        ESPNow.CMD_RST= b'\xff\xff'
        ESPNow.CMD_ACK= b'\xff\xfe'
        ESPNow.CMD_BOOT= b'\xff\x00'
        ESPNow.CMD_STOP = b'\xf4\xfe'
        ESPNow.CMD_FILE= b'\xf4\x10'
        ESPNow.CMD_DONE= b'\xf4\x11'
        ESPNow.CMD_FILE_WRITE_ACK= b'\xf4\x12'
        sta = network.WLAN(network.STA_IF); sta.active(False)
        ap = network.WLAN(network.AP_IF); ap.active(False)
        sta.active(True)
        while not sta.active():
            time.sleep(0.1)
        sta.disconnect()   # For ESP8266
        self.e = espnow.ESPNow()
        self.e.active(True)
        self.peer_mac = network.WLAN().config('mac')
        self.peer_mac_str = (ubinascii.hexlify(self.peer_mac, ':').decode())
        self.e.add_peer(self.peer_mac)
        self.nodeMap = {}
        self.callback = None
        self.file_buffer = {}

    def cmd(self,msg):
        if msg == ESPNow.CMD_STOP:
            return "STOP"
        elif msg == ESPNow.CMD_RST:
            return "RST"
        elif msg == ESPNow.CMD_BOOT:
            return "BOOT"
        elif msg[0:2] == ESPNow.CMD_FILE:
            return "FILE"
        elif msg[0:2] == ESPNow.CMD_FILE_WRITE_ACK:
            return "CMD_FILE_WRITE_ACK"
        elif msg == ESPNow.CMD_ACK:
            return "ACK"
        elif msg == ESPNow.CMD_DONE:
            return "DONE"
        return f"UNKNOWN: {msg}"
    
    def join(self,peer_data):
        peer = ''
        if isinstance(peer_data, bytes):
            peer = peer_data
        else:
            data = peer_data.split(':')
            peer = bytes([int(part, 16) for part in data])

        try: # maybe already join
            peer_str =':'.join(f'{byte:02x}' for byte in peer)
            self.nodeMap[peer_str] = peer
            #print(f"save:[{self.nodeMap}]")
            self.e.add_peer(peer)
        except Exception as e:
            pass#print(e)

    def sendCmd(self, cmd , peer_mac_str):
        print(f"-> [{peer_mac_str}] cmd:{self.cmd(cmd)}")
        if peer_mac_str in self.nodeMap:
            #print(f"send cmd: {cmd}")
            # 將 peer_data 分割成列表
            data = peer_mac_str.split(':')
            # 將每個十六進制字符串轉換為整數，然後組合成 bytes 對象
            peer = bytes([int(part, 16) for part in data])
            self.e.send(peer, cmd)

    def sendAll(self, message):
        for peer_mac in self.nodeMap.keys():
            self.e.send(self.nodeMap[peer_mac], message)

    def broadcast(self, message):
        self.e.send(b'\xff\xff\xff\xff\xff\xff', message)
        #print("mac:"+ubinascii.hexlify(self.peer_mac).decode())

    def broadcast_mac(self):
        print(f"-> [ff:ff:ff:ff:ff:ff] cmd: {self.cmd(ESPNow.CMD_BOOT)}")
        self.e.send(b'\xff\xff\xff\xff\xff\xff', ESPNow.CMD_BOOT) # boot

    def recv(self, callback=None):
        self.callback = callback

    def irecv(self, recvTime):
        peer, msg = self.e.irecv(int(recvTime * 1000))

        if not msg == None:
            gc.collect()
            peer_str = ':'.join(f'{byte:02x}' for byte in peer)
            self.join(peer_str)
            if len(msg) == 2:
                print(f"<- [{peer_str}] cmd: {self.cmd(msg)}")
                if msg == ESPNow.CMD_RST:
                    machine.reset()
                    
                elif msg == ESPNow.CMD_STOP:
                    self.sendCmd(ESPNow.CMD_ACK, peer_str)
                    self.irecv(900)
                
            elif len(msg) > 4 and msg[0:2] == ESPNow.CMD_FILE:
                print(f"<- [{peer_str}] cmd: {self.cmd(msg)}")
                # 这是内部控制指令（接收文件）
                chunk_size = msg[2]
                total_length = int.from_bytes(msg[3:7], 'big')
                end_of_filename = bytearray_find(msg, b'\n', 7)
                filename = msg[7:end_of_filename].decode()
                start_byte = int.from_bytes(msg[end_of_filename + 1:end_of_filename + 3], 'big')
                file_data = msg[end_of_filename + 3:]
                if filename not in self.file_buffer:
                    self.file_buffer[filename] = bytearray(total_length)
                self.file_buffer[filename][start_byte:start_byte + len(file_data)] = file_data
                # 检查是否所有区块都已接收
                #print(f"file: {(start_byte + len(file_data))} / {total_length}")
                if total_length == (start_byte + len(file_data)):
                    # 文件已完整，写入文件
                    with open(filename, 'wb') as f:
                        f.write(self.file_buffer[filename])
                    self.file_buffer = {}
                    gc.collect()
                    print("File " + filename + " written successfully")
                    self.sendCmd(ESPNow.CMD_FILE_WRITE_ACK, peer_str)
                    self.sendCmd(ESPNow.CMD_DONE, peer_str)
                else:
                    self.sendCmd(ESPNow.CMD_FILE_WRITE_ACK, peer_str)
            else:
                # 非内部控制指令，调用用户提供的回调
                if self.callback is not None:
                    self.callback(peer, msg, self.e.peers_table)

def bytearray_find(haystack, needle, start=0):
    needle_len = len(needle)
    for i in range(start, len(haystack) - needle_len + 1):
        if haystack[i:i + needle_len] == needle:
            return i
