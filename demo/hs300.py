import os, usocket, time, ubinascii, network, machine
import usocket as socket
import ustruct as struct
import uasyncio as asyncio

def do_connect():
    global connected
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print('connecting to network...')
    #sta_if.disconnect()
    if(not sta_if.isconnected()):
        sta_if.connect('KingKit_MeetingRoom', 'webduino')
    cnt = 0
    while not sta_if.isconnected():
        cnt = cnt + 1
        time.sleep(0.5)
        if cnt == 60:
            break
    connected = sta_if.isconnected()
    print('network config:', sta_if.ifconfig())



class TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(10)
        self.received_buffers = []
        self.total_length = None
        self.received_length = 0

    async def connect(self):
        addr_info = socket.getaddrinfo(self.host, self.port)
        addr = addr_info[0][-1]
        self.client.connect(addr)
        print(f'Connected to: {self.host}:{self.port}')

    def handle_data(self, data):
        print('Raw received data:', data)

        # 将接收到的数据加入缓存
        self.received_buffers.append(data)
        self.received_length += len(data)

        # 读取数据长度
        if self.total_length is None and self.received_length >= 4:
            combined_buffer = b''.join(self.received_buffers)
            self.total_length = struct.unpack('>I', combined_buffer[:4])[0]

            # 如果只有长度信息，更新缓存
            if self.received_length == 4:
                self.received_buffers = [combined_buffer[4:]]
            else:
                self.received_buffers = [combined_buffer[4:]]

            self.received_length -= 4

        # 读取实际的数据部分
        if self.total_length is not None and self.received_length >= self.total_length:
            combined_buffer = b''.join(self.received_buffers)
            encrypted_response = combined_buffer[:self.total_length]

            # 解密接收到的数据
            try:
                decrypted_data = self.decrypt(encrypted_response).decode('utf-8')
                print('Received (decrypted):', decrypted_data)
                return decrypted_data
            except Exception as error:
                print('Error decrypting data:', error)
                raise error

            # 重置缓存和长度
            self.received_buffers = []
            self.total_length = None
            self.received_length = 0

    async def send_cmd(self, payload_string):
        # 加密消息
        encrypted_payload = self.encrypt(payload_string)

        # 创建一个 Buffer 来包含长度信息和加密消息
        message_length = struct.pack('>I', len(encrypted_payload))

        # 将长度信息和加密消息合并
        full_message = message_length + encrypted_payload

        # 打印并发送完整消息
        print('Sending full message:', full_message)
        self.client.sendall(full_message)

        data = self.client.recv(4096)
        return self.handle_data(data)

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
        print('Client connection closed')

# 使用示例
async def main():
    client = TCPClient('192.168.0.4', 9999)
    await client.connect()
    
    # 发送获取系统信息的命令
    plugs = await client.send_cmd('{"system":{"get_sysinfo":{}}}')
    print('System Info:', plugs)

    # 发送控制命令
    resp = await client.send_cmd('{"system":{"set_relay_state":{"state":1}},"context":{"child_ids":["80061A22885883270C47B5D53B02BB402258969001"]}}')
    print('Command Response:', resp)

    # 关闭连接
    client.close()

# 运行示例
do_connect()
asyncio.run(main())

