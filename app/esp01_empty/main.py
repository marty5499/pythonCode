import espnow, ubinascii, network, machine

def callback(peer,msg):
    print(msg)

esp.recv(callback)
print("ready")

while True:
    esp.irecv(1)
