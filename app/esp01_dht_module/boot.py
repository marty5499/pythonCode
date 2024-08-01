import uos, machine, gc, time
from webduino.espnow_8266 import ESPNow

esp = ESPNow()
print("[MAC] " + esp.peer_mac_str)
esp.recv()

esp.recv()
esp.broadcast_mac()
esp.irecv(1)
#esp.broadcast_mac()
#esp.irecv(1)
#esp.broadcast_mac()
#esp.irecv(1)



