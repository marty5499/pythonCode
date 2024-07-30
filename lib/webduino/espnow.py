import espnow, ubinascii, network
import machine, time

class ESPNow:
    def __init__(self, peer_str = None):
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        self.e = espnow.ESPNow() 
        self.e.active(True)
        if not peer_str == None:
            if isinstance(peer_str, bytes):
                self.peer_mac = peer_str
                hex_string = ''.join(f'{byte:02x}' for byte in peer_str)
                print(f"join {peer_str}:{hex_string}")
            else:
                peer_hex = ''.join('{:02x}'.format(ord(char)) for char in peer_str)
                peer_mac = ubinascii.unhexlify(peer_hex)
                if len(peer_mac) != 6:
                    raise ValueError("ESPNow: bytes or bytearray wrong length")
                formatted_hex = ''.join(f'\\x{peer_hex[i:i+2]}' for i in range(0, len(peer_hex), 2))
                print(f"join {peer_str}:{formatted_hex}")
                self.peer_mac = peer_mac
        else:
            print("broadcast node")
            self.peer_mac = b'\xff\xff\xff\xff\xff\xff'
        self.e.add_peer(self.peer_mac)
        self.file_buffer = {}

    def send(self, message):
        self.e.send(self.peer_mac, message)
        #print("mac:"+ubinascii.hexlify(self.peer_mac).decode())



    def recv(self, callback=None):
        def bytearray_find(haystack, needle, start=0):
            needle_len = len(needle)
            for i in range(start, len(haystack) - needle_len + 1):
                if haystack[i:i + needle_len] == needle:
                    return i
            return -1        
        def internal_recv_callback(*args):
            if len(args) ==1:
                code = 1 # nonuse
                peer, msg = args[0].recv()
            else:
                code = args[0]
                peer, msg = args[1]
            peer_str = ''.join(f'{byte:02x}' for byte in peer)
            print(f"src[{peer_str}] cmd: {msg[0]:02x},{msg[1]:02x}")
            #"""
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
                # 非内部控制指令，调用用户提供的回调
                if callback is not None:
                    callback(peer, msg, self.e.peers_table)
            #"""
        self.e.irq(internal_recv_callback)

    def sendFile(self, file_path, target_file, chunk_size, callback=None):
        with open(file_path, 'rb') as f:
            file_content = f.read()

        total_length = len(file_content)
        total_chunks = (total_length + chunk_size - 1) // chunk_size
        for chunk_index in range(total_chunks):
            start_byte = chunk_index * chunk_size
            end_byte = min(start_byte + chunk_size, total_length)
            chunk_data = file_content[start_byte:end_byte]

            message = bytearray([0xf4, 0x10])
            message.append(chunk_size)  # 這邊加入此次傳送的 chunk_size
            message.extend(total_length.to_bytes(4, 'big'))  # 修正這裡，傳送總長度
            message.extend(target_file.encode() + b'\n')
            message.extend(start_byte.to_bytes(2, 'big'))
            message.extend(chunk_data)
            self.send(message)
            if callback is not None:
                callback(self.peer_mac , str(start_byte).encode() , self.e.peers_table)


    def cmd_reset(self):
        message = bytearray([0xf4, 0xff])
        self.send(message)
        print("Reset command sent")
