from machine import Pin
import time, espnow, ubinascii, network, machine, urandom

class ESPNow:
    def __init__(self):
        self.e = None
        self.peer_mac = None

    def init(self):
        sta = network.WLAN(network.STA_IF)
        sta.active(True)
        self.e = espnow.ESPNow()
        self.e.active(True)
        print("ESPNow initialized")

    def join(self, peer_str):
        peer_hex = ''.join('{:02x}'.format(ord(char)) for char in peer_str)
        peer_mac = ubinascii.unhexlify(peer_hex)
        if len(peer_mac) != 6:
            raise ValueError("ESPNow: bytes or bytearray wrong length")
        formatted_hex = ''.join(f'\\x{peer_hex[i:i+2]}' for i in range(0, len(peer_hex), 2))
        print(f"Peer {peer_str} (hex: {formatted_hex}) added")
        self.peer_mac = peer_mac
        self.e.add_peer(self.peer_mac)

    def send(self, message):
        if self.peer_mac:
            self.e.send(self.peer_mac, message.encode())
            print(f"Message '{message}' sent to {self.peer_mac}")
        else:
            print("No peer joined. Please join a peer first.")


# Example usage
esp_now = ESPNow()
esp_now.init()
esp_now.join('wa1234')  # Adding peer
esp_now.send('okok')
