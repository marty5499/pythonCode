import usocket as socket
import ustruct as struct
import ujson as json
import os, time, ubinascii, network, machine

class ConnectionError(Exception):
    pass

class HS300:
    def __init__(self, host, port=9999):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(10)
        self.received_buffers = []
        self.total_length = None
        self.received_length = 0
        self.children = []

    def connect(self):
        try:
            addr_info = socket.getaddrinfo(self.host, self.port)
            addr = addr_info[0][-1]
            self.client.connect(addr)
            #print(f'Connected to: {self.host}:{self.port}')
        except OSError as e:
            print(f'Failed to connect to {self.host}:{self.port}')
            return
        
        # 获取系统信息
        sysinfo = self.send_cmd('{"system":{"get_sysinfo":{}}}')
        if sysinfo is None:
            raise ConnectionError("Failed to retrieve system information")
        sysinfo_json = json.loads(sysinfo)
        self.children = sysinfo_json['system']['get_sysinfo']['children']
        #print('debug:children:', self.children)

    def handle_data(self, data):
        # 将接收到的数据加入缓存
        self.received_buffers.append(data)
        self.received_length += len(data)
        #print(f'Received data length: {self.received_length}')

        # 读取数据长度
        if self.total_length is None and self.received_length >= 4:
            combined_buffer = b''.join(self.received_buffers)
            self.total_length = struct.unpack('>I', combined_buffer[:4])[0]
            #print(f'Total message length: {self.total_length}')

            # 更新缓存去掉长度信息部分
            self.received_buffers = [combined_buffer[4:]]
            self.received_length -= 4

        # 读取实际的数据部分
        if self.total_length is not None and self.received_length >= self.total_length:
            combined_buffer = b''.join(self.received_buffers)
            encrypted_response = combined_buffer[:self.total_length]
            #print(f'Encrypted response: {encrypted_response}')

            # 解密接收到的数据
            try:
                decrypted_data = self.decrypt(encrypted_response).decode('utf-8')
                #print('debug:Received:', decrypted_data)
                # 重置缓存和长度
                self.received_buffers = []
                self.total_length = None
                self.received_length = 0
                return decrypted_data
            except Exception as error:
                print('Error decrypting data:', error)
                return None

        return None

    def send_cmd(self, payload_string):
        # 打印未加密的消息
        #print('debug:Sending:', payload_string)
        
        # 加密消息
        encrypted_payload = self.encrypt(payload_string)

        # 创建一个 Buffer 来包含长度信息和加密消息
        message_length = struct.pack('>I', len(encrypted_payload))

        # 将长度信息和加密消息合并
        full_message = message_length + encrypted_payload

        # 发送完整消息
        self.client.sendall(full_message)

        # 接收响应数据
        while True:
            data = self.client.recv(4096)
            if not data:
                print("No data received")
                return None
            response = self.handle_data(data)
            if response is not None:
                return response

    # 加密函数
    def encrypt(self, input, first_key=0xab):
        buf = bytearray(input.encode('utf-8'))
        key = first_key
        for i in range(len(buf)):
            buf[i] ^= key
            key = buf[i]
        return bytes(buf)

    # 解密函数
    def decrypt(self, input, first_key=0xab):
        buf = bytearray(input)
        key = first_key
        for i in range(len(buf)):
            next_key = buf[i]
            buf[i] ^= key
            key = next_key
        return bytes(buf)

    # 关闭连接
    def close(self):
        self.client.close()
        #print('Client connection closed')

    # 获取端口状态
    def port_status(self, port_number):
        if port_number < 0 or port_number >= len(self.children):
            return "Invalid port number"
        return "on" if self.children[port_number]['state'] == 1 else "off"

    # 设置端口开关
    def sw(self, port_number, state):
        if port_number < 0 or port_number >= len(self.children):
            return False
        
        port_id = self.children[port_number]['id']
        cmd = json.dumps({
            "system": {
                "set_relay_state": {
                    "state": state
                }
            },
            "context": {
                "child_ids": [port_id]
            }
        })
        
        response = self.send_cmd(cmd)
        if response is None:
            return False
        response_json = json.loads(response)
        err_code = response_json['system']['set_relay_state']['err_code']

        # 更新当前端口的状态
        if err_code == 0:
            self.children[port_number]['state'] = state
        
        return err_code == 0