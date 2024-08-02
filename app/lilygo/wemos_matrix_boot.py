from webduino.espnow_8266 import ESPNow
import time

esp = ESPNow()

print("[MAC] " + esp.peer_mac_str)

esp.recv()
esp.broadcast_mac()
esp.irecv(1)
#esp.broadcast_mac()
#esp.irecv(1)
#esp.broadcast_mac()
#esp.irecv(1)

