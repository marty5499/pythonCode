import espnow, ubinascii, network
import machine, time

class ESPNow:
    def __init__(self):
        sta = network.WLAN(network.STA_IF); sta.active(False)
        ap = network.WLAN(network.AP_IF); ap.active(False)
        sta.active(True)
        while not sta.active():
            time.sleep(1)
        sta.disconnect()   # For ESP8266
        while sta.isconnected():
            time.sleep(1)
        sta.active(False)
        ap.active(True)
        self.e = espnow.ESPNow()
        self.e.active(True)
        self.peer_mac = network.WLAN().config('mac')
        print(ubinascii.hexlify(network.WLAN().config('mac'),':').decode())
        self.e.add_peer(self.peer_mac)
        self.file_buffer = {}

    def send(self, message):
        if self.peer_mac:
            self.e.send(self.peer_mac, message)
            print("Sent to "+str(self.peer_mac))
        else:
            print("No peer joined. Please join a peer first.")

    def irecv(self, recvTime):
        peer, msg = self.e.irecv(int(recvTime*1000))
        if not msg == None:
            #print(f"{msg[0]:02x},{msg[1]:02x}")
            if len(msg) == 2 and msg[0] == 0xf4 and msg[1] == 0xff:
                machine.reset()
            elif len(msg) > 4 and msg[0] == 0xf4 and msg[1] == 0x10:
                # 这是内部控制指令（接收文件）
                chunk_size = msg[2]
                total_length = int.from_bytes(msg[3:7], 'big')
                end_of_filename = msg.find(b'\n', 7)
                filename = msg[7:end_of_filename].decode()
                start_byte = int.from_bytes(msg[end_of_filename + 1:end_of_filename + 3], 'big')
                file_data = msg[end_of_filename + 3:]

                if filename not in self.file_buffer:
                    self.file_buffer[filename] = bytearray(total_length)

                self.file_buffer[filename][start_byte:start_byte + len(file_data)] = file_data
                # 檢查是否所有區塊都已接收
                if total_length == (start_byte+len(file_data)):
                    # 文件已完整，寫入文件
                    with open(filename, 'wb') as f:
                        f.write(self.file_buffer[filename])
                    print("File "+filename+" written successfully")

            else:
                # 非内部控制指令，调用用户提供的回调
                print("callback")
                if callback is not None:
                    callback(peer, msg)



    def cmd_reset(self):
        message = bytearray([0xf4, 0xff])
        self.send(message)
        print("Reset command sent")

