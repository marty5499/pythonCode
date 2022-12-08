import os, usocket, time, ubinascii, network, machine

sta = network.WLAN(network.STA_IF)
sta.active(True)
print('connecting to network...')
if(not sta.isconnected()):
    sta.connect('KingKit_2.4G', 'webduino')
cnt = 0
while not sta.isconnected():
    cnt = cnt + 1
    time.sleep(0.5)
    if cnt == 60:
        break

sta.disconnect()
print("isConnect:"+str(sta.isconnected()))
