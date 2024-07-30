import espnow, ubinascii, network
import machine, time

class ESPNow:
    def __init__(self):
        sta = network.WLAN(network.STA_IF)
        sta.active(True)        
        self.e = espnow.ESPNow()
        self.e.active(True)
        self.peer_mac = network.WLAN().config('mac')
        print(ubinascii.hexlify(network.WLAN().config('mac'), ':').decode())
        self.e.add_peer(self.peer_mac)
        self.file_buffer = {}

    def send(self, message):
        self.e.send(self.peer_mac, message)
        #print("Sent to " + str(self.peer_mac))

    def irecv(self, recvTime):
        peer, msg = self.e.irecv(int(recvTime * 1000))
        if not msg == None:
            if len(msg) == 2 and msg[0] == 0xf4 and msg[1] == 0xff:
                machine.reset()
            elif len(msg) > 4 and msg[0] == 0xf4 and msg[1] == 0x10:
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
                if total_length == (start_byte + len(file_data)):
                    # 文件已完整，写入文件
                    with open(filename, 'wb') as f:
                        f.write(self.file_buffer[filename])
                    print("File " + filename + " written successfully")
                    time.sleep(2)
                    machine.reset()
                else:
                    self.irecv(3)


def bytearray_find(haystack, needle, start=0):
    needle_len = len(needle)
    for i in range(start, len(haystack) - needle_len + 1):
        if haystack[i:i + needle_len] == needle:
            return i
    return -1
