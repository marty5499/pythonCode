from webduino.board import Board
from webduino.led import LED
import ntptime,time, machine, urequests, gc, os, ussl
from webduino.camera import Camera
import usocket

class FileBrowser:

    def initCamera(ledPin=4):
        print("cam init...")
        led = LED(ledPin)
        led.blink(0.25)
        Camera.init()
        led.blink(0)
        gc.collect()
        
    def procResponse(s):
        l = s.readline()
        #print("resp>>>"+l.decode("utf-8"))
        l = l.split(None, 2)
        status = int(l[1])
        respHeader = ""
        respBody = ""
        contentLength = -1
        isHeader = True
        if len(l) > 2:
            reason = l[2].rstrip()
        while True:
            l = s.readline().decode("utf-8")
            print("resp:%s"%l)
            if(l == "\r\n"):
                isHeader = False
            else:
                if(isHeader):
                    if(l.startswith('Content-Length: ')):
                        contentLength = int(l.split(' ')[1])
                    respHeader += l
                else:
                    respBody += l
                    if(len(respBody) == contentLength):
                        break
            if len(l)>9 and l[0:9]=='Location:': response = l[10:-2]
            if not l or l == "\r\n\r\n": break
        s.close()
        return [respHeader,respBody]
    

    def login(username,password):
        host ='filebrowser.webduino.tw'
        path = 'filebrowser/api/login'
        port = 443
        data = '{"username":"'+username+'","password":"'+password+'","recaptcha":""}'
        ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
        ai = ai[0]
        s = usocket.socket(ai[0], ai[1], ai[2])
        s.connect(ai[-1])
        s = ussl.wrap_socket(s, server_hostname=host)
        s.write(b"%s /%s HTTP/1.0\r\n" % ("POST", path))
        s.write(b"Host: %s\r\n" % host)
        s.write(b"Content-Length: %d\r\n" % len(data))
        s.write(b"Content-Type: application/json\r\n")
        s.write(b"\r\n")
        s.write(data)
        resp = FileBrowser.procResponse(s)
        FileBrowser.token = resp[1]
        return resp[1]

# https://filebrowser.webduino.tw/filebrowser/api/resources/img.jpg?override=true
# https://filebrowser.webduino.tw/filebrowser/api/resources/img.jpg?override=false
    def upload(image,filename):
        host = 'filebrowser.webduino.tw'
        path = 'filebrowser/api/resources/%s?override=true' % filename
        port = 443
        ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
        ai = ai[0]
        s = usocket.socket(ai[0], ai[1], ai[2])
        s.connect(ai[-1])
        s = ussl.wrap_socket(s, server_hostname=host)
        #print("https://%s/%s" % (host,path))
        s.write(b"%s /%s HTTP/1.1\r\n" % ("POST", path))
        s.write(b"Host: %s\r\n" % host)
        s.write(b"x-auth: %s\r\n" % FileBrowser.token)
        s.write(b"Content-Length: %d\r\n" % len(image))
        s.write(b"Content-Type: application/octet-stream\r\n")
        s.write(b"\r\n")
        s.write(image)
        return FileBrowser.procResponse(s)

#####################
try:
    import cmd
    machine.reset()
except:
    pass
#####################
try:
    print("==")
    print("-=-=-=-= base =-=-=-=-")
    print("==")
    board = Board(devId='0911')
    FileBrowser.initCamera()
    img = Camera.capture()
    print("img size: %d" % len(img))
    print("login...")
    FileBrowser.login('admin','wa525420')[1]
    print("fileUpload...")
    resp = FileBrowser.upload(img,'okok123.jpg')
    print("body:%s"%resp[1])
    #board.loop()
except Exception as e:
    print(e)
    print('')
    machine.reset()