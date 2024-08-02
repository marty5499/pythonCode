import espnow, ubinascii, network, machine

def callback(peer,msg):
    print(msg)
"""
白: 13 <--> DIN
藍: 14 <--> CLK
灰: 15 <--> CS
"""

esp.recv(callback)
print("ready")

while True:
    esp.irecv(1)

