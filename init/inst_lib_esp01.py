import os, usocket, time, ubinascii, network, machine

class Response:

    def __init__(self, f, file=None):
        self.raw = f
        self.encoding = "utf-8"
        self._cached = None
        self.file = file

    def close(self):
        if self.raw:
            self.raw.close()
            self.raw = None
        self._cached = None

    @property
    def content(self):
        if self._cached is None:
            try:
                gc.collect()
                if self.file is not None:
                    defSize = 512
                    ba = bytearray(defSize)
                    f = open(self.file,"w+")
                    rSize = 0
                    while True:
                        readSize = self.raw.readinto(ba)
                        f.write(ba,readSize)
                        rSize = rSize + readSize
                        if readSize < defSize:
                            break
                    f.close()
                    self._cached = str(rSize)
                else:
                    self._cached = self.raw.read()
            finally:
                self.raw.close()
                self.raw = None
        return self._cached

    @property
    def text(self):
        return str(self.content, self.encoding)

    def json(self):
        import ujson
        return ujson.loads(self.content)


def request(method, url, data=None, json=None, headers={}, stream=None, file=None):
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    elif proto == "https:":
        import ussl
        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)

    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)
    #print("host:",host,",port:",port)
    ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
    ai = ai[0]

    s = usocket.socket(ai[0], ai[1], ai[2])
    try:
        s.connect(ai[-1])
        if proto == "https:":
            s = ussl.wrap_socket(s, server_hostname=host)
        s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
        if not "Host" in headers:
            s.write(b"Host: %s\r\n" % host)
        # Iterate over keys to avoid tuple alloc
        for k in headers:
            s.write(k)
            s.write(b": ")
            s.write(headers[k])
            s.write(b"\r\n")
        if json is not None:
            assert data is None
            import ujson
            data = ujson.dumps(json)
            s.write(b"Content-Type: application/json\r\n")
        if data:
            s.write(b"Content-Length: %d\r\n" % len(data))
        s.write(b"\r\n")
        if data:
            s.write(data)

        l = s.readline()
        #print(l)
        l = l.split(None, 2)
        status = int(l[1])
        reason = ""
        if len(l) > 2:
            reason = l[2].rstrip()
        while True:
            l = s.readline()
            if not l or l == b"\r\n":
                break
            #print(l)
            if l.startswith(b"Transfer-Encoding:"):
                if b"chunked" in l:
                    raise ValueError("Unsupported " + l)
            elif l.startswith(b"Location:") and not 200 <= status <= 299:
                raise NotImplementedError("Redirects not yet supported")
    except OSError:
        s.close()
        raise

    resp = Response(s, file=file)
    resp.status_code = status
    resp.reason = reason
    return resp


def head(url, **kw):
    return request("HEAD", url, **kw)

def get(url, **kw):
    return request("GET", url, **kw)

def save(url, **kw):
    return request("GET", url, **kw)

def post(url, **kw):
    return request("POST", url, **kw)

def put(url, **kw):
    return request("PUT", url, **kw)

def patch(url, **kw):
    return request("PATCH", url, **kw)

def delete(url, **kw):
    return request("DELETE", url, **kw)


class Res:

    def save(url,file):
        try:
            response = get(url)
            print(">>",len(response.text) )
            print("get file:",file,'size:',len(response.text),',save to:',file)
            f = open(file, 'w')
            f.write(response.text)
            f.close()
            print("OK.")
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(e)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        

    def get(path,file):
        try:
            response = save('https://marty5499.github.io/pythonCode/'+path,file=file)
            print("get file:",file,'size:',response.text,',save to:',path)
            print("OK:,mem:%d" % gc.mem_free())
        except Exception as e:
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print(e)
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


    def exe(dir):
        srcDir = dir
        try:
            while True:
                idx = dir.index('/')
                try:
                    name = dir[0:idx]
                    try:
                        print('mkdir',name)
                        os.mkdir(name)
                    except:
                        pass
                    try:
                        os.chdir(name)
                        print('cd',name)
                    except:
                        pass
                except:
                    pass
                dir = dir[idx+1:]
        except:
            pos = -1
            try:
                pos = dir.index('.mpy')
            except:
                pass
            try:
                if pos == -1:
                    pos = dir.index('.py')
            except:
                pass
            try:
                if pos > 0:
                    pyFile = dir
                    Res.get(srcDir,pyFile)
                else:
                    try:
                        print("mkdir",dir)
                        os.mkdir(dir)
                    except:
                        pass
                    try:
                        os.chdir(dir)
                        print("cd ",dir)
                    except:
                        pass
            except:
                pass
        os.chdir('/')

def do_connect():
    print("connect...")
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

def download_demo():
    try:
        os.mkdir('demo')
    except:
        pass
    
    print("get demo files...")
    files = [
        'demo_adxl345.py',
        'demo_qmc5883.py',
        'demo_buzzer.py',
        'demo_dht.py',
        'demo_dfplayermini.py',
        'demo_lcd1602.py',
        'demo_rotary.py',
        'demo_max7219.py',
        'demo_mlx90614.py',
        'demo_ssd1306.py',
        'demo_tm1637.py',
        'demo_ultrasonic.py',
        'demo_ws2812.py',
        'demo_servo.py',
        ]

    for file in files:
        Res.get('esp01/'+file,'demo/'+file)


def setup_info(deviceId='',board_devSSID=''):
    from webduino.config import Config
    #Utils.save('https://marty5499.github.io/pythonCode/init/boot.py','boot.py')
    Res.get('init/boot.py','boot.py')
    Config.load()
    if(not deviceId == ''):
        Config.data['devId'] = deviceId
    else:
        deviceId = Config.data['devId']
        
    if(not board_devSSID == ''):
        Config.data['devSSID'] = board_devSSID
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    print("-    Device ID: [ %s ]    -" % deviceId)
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
    Config.save()
    """
    print('Mac address:',ubinascii.hexlify(network.WLAN().config('mac'),':').decode())    
    """

def inst_library():
    # 開源必備
    Res.exe('lib/urequests.py')
    Res.exe('lib/umqtt/simple.py')
    # 小米燈泡
    Res.exe('lib/uyeelight.py')
    # Webduino 類別庫
    Res.exe('lib/webduino/led.py')
    Res.exe('lib/webduino/config.py')
    Res.exe('lib/webduino/gdriver.py')
    #Res.exe('lib/webduino/camera.py')
    Res.exe('lib/webduino/board.py')
    Res.exe('lib/webduino/mqtt.py')
    Res.exe('lib/webduino/wifi.py')
    Res.exe('lib/webduino/webserver.py')
    Res.exe('lib/webduino/debug.py')
    Res.exe('lib/utils.py') # save url to file
    Res.get('','index.html')
    # 傳感器
    Res.exe('lib/ahtx0.py') # 溫濕度
    Res.exe('lib/adxl345.py') # save url to file
    Res.exe('lib/hmc5883l.py') # save url to file
    Res.exe('lib/QMC5883.py') # save url to file
    Res.exe('lib/mfrc522.py') # save url to file
    Res.exe('lib/mlx90614.py') # save url to file
    Res.exe('lib/RFBtn.py') # save url to file
    Res.exe('lib/max7219.py') # save url to file
    Res.exe('lib/ssd1306.py') # save url to file
    Res.exe('lib/TM1637.py') # save url to file
    Res.exe('lib/uyeelight.py') # save url to file
    Res.exe('lib/dfplayer.py') # save url to file
    Res.exe('lib/dfplayermini.py') # mp3
    # rotary
    Res.exe('lib/rotary.py')
    Res.exe('lib/rotary_irq_esp.py')
    Res.exe('lib/hcsr04.py') # ultrasonic
    # LCD1602
    Res.exe('lib/lcd_api.py')
    Res.exe('lib/i2c_lcd.py') # save url to file
    # TTGO
    Res.exe('lib/st7789.py') # save url to file
    Res.exe('lib/st7789py.py') # save url to file
    Res.exe('lib/sysfont.py') # save url to file
    
    Res.get('','index.html')


def install():
    id = 'aa'
    do_connect()
    inst_library()
    download_demo()
    setup_info(deviceId = id , board_devSSID = id)

install()