import uos, usocket, time, ubinascii, network, machine, gc

time.sleep(1.5)

import webrepl
uos.dupterm(None, 1)
webrepl.start()
gc.collect()



def do_connect():
    global connected
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    print('connecting to network...')
    #sta_if.disconnect()
    if(not sta_if.isconnected()):
        sta_if.connect('KingKit_2.4G', 'webduino')
    cnt = 0
    while not sta_if.isconnected():
        cnt = cnt + 1
        time.sleep(0.5)
        if cnt == 60:
            break
    connected = sta_if.isconnected()
    print('network config:', sta_if.ifconfig())

do_connect()
