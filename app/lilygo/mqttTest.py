from webduino.board import Board

esp = ESPNow()
esp.recv(callback)
ed.text('Ready...',10,10)

def ctrl(topic,msg):
    try:
        print(">> " + msg)
        ed.text(msg,10,30)
        s3.pub('b01/pub','['+msg+']')
        #esp.broadcast(msg)
        esp.sendAll(msg)
    except Exception as e:
        print(e)

s3 = Board()
s3.start(checkTime=0.05)
ed.text('connect...',10,10)
print('connect..')
s3.onTopic('b01/mybit',ctrl)
ed.text('init...ok',10,10)
print("init...ok")
"""
while True:
    s3.check()
    time.sleep(0.05)
"""