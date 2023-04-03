from webduino.wifi import WiFi
from webduino.mqtt import MQTT
from webduino.debug import debug
from webduino.config import Config
from webduino.webserver import WebServer
import time, ubinascii, network, machine, os
from machine import Timer

class Board:
    
    Ver = '0.2.3b'
    def __init__(self,devId=''): 
        self.wifi = WiFi
        self.mqtt = MQTT
        self.wifi.onlilne(self.online)
        self.topics = {}
        self.topic_report = 'waboard/state'
        self.config = Config
        self.now = 0
        json = self.config.load()
        if(devId == ''): devId = json['devId']
        json['devId'] = devId
        debug.print("Device ID:"+devId)
        self.config.save()
        self.devId = devId
        self.devPasswd = json['devPasswd']
        self.topic_cmd = self.devId+'/cmd'
        self.enableAP()
        self.connect(ssid=json['ssid1'],pwd=json['passwd1'])
        debug.print('board IP:'+self.ip())

    def ap(self):
        return self.wifi.ssid

    def ip(self):
        return self.wifi.ip

    def mac(self):
        return ubinascii.hexlify(network.WLAN().config('mac'),':').decode()

    def enableAP(self):
        ssid = self.config.data['devSSID']
        pwd = self.config.data['devPasswd']
        self.wifi.enableAP(ssid,pwd)
        self.wifi.web = WebServer(self,80)
        self.wifi.web.listener()
        debug.print("webServer start...")
    
    def online(self,status):
        if status:
            self.mqtt.connect()
            debug.print("connect mqtt...OK")
        else:
            debug.print("offline...")
            pass
        
    def connect(self,ssid='webduino.io',pwd='webduino'):
        while True:
            if self.wifi.connect(ssid,pwd):
                break
        debug.print("WiFi Ready , MQTT Ready , ready to go...")
        self.mqtt.sub(self.devId+"/#",self.dispatch)
        self.mqtt.set_last_will(self.topic_report, 'disconnect', retain=True, qos=1)
        self.onTopic('cmd',self.execCmd)
        self.report('boot')
        return self
        
    def onTopic(self,topic,cbFunc):
        self.topics[topic] = cbFunc
        
    def dispatch(self,topic,msg):
        topic = topic.decode("utf-8")
        msg = msg.decode("utf-8")
        #_topic = topic.replace(self.devId+"/",'')
        debug.print("topic:"+topic+",msg:"+msg)
        self.topics[topic](topic,msg)
    
    def publish(self,topic,msg):
        self.mqtt.pub(topic,msg)

    def pub(self,topic,msg):
        self.mqtt.pub(topic,msg)
        
    def start(self,checkTime=0.25):
        self.chk = Timer(0)
        self.chk.init(period=int(checkTime*1000), mode=Timer.PERIODIC, callback=lambda t:self.check())
        
    def loop(self):
        debug.print("run...")
        while True:
            self.check()
            time.sleep(0.1)

    def check(self):
        self.mqtt.checkMsg()
        self.now = self.now + 1
        if self.now % 300 == 0:
            #print("mqtt ping...")
            try:
                self.mqtt.client.ping()
            except:
                #print("mqtt broken!")
                pass
        if self.now % 600 == 0:
            debug.print("wifi check...",self.wifi.checkConnection(self.now))
            self.now = 0        
        
    def ping(self):
        self.mqtt.client.ping()

    def report(self,cmd):
        report = cmd + ' '+self.devId
        debug.print("publish["+self.topic_report+"] "+report)
        self.mqtt.pub(self.topic_report,report)
        debug.print("publish OK")
    
    def setExtraCmdProcess(self,cb):
        Board.extraCmd = cb
        
    def extraCmd(cmd,dataArgs):
        pass
        
    def execCmd(self,data):
        dataArgs = data.split(' ')
        debug.print("exceCmd:",dataArgs)
        cmd = dataArgs[0]
        
        if cmd == 'reboot':
            self.report('reboot')
            time.sleep(1)
            debug.print("restart...")
            machine.reset()

        elif cmd == 'ping':
            self.report('pong')

        elif cmd == 'reset':
            os.remove('main.py')
            self.report('reset')
            time.sleep(1)
            machine.reset()

        # save https://xx.xx/test.py main.py 
        elif cmd == 'save':
            url = dataArgs[1]
            file = dataArgs[2]
            f = open('cmd.py','w')
            f.write('import os\r\n')
            f.write('os.remove("cmd.py")\r\n')
            f.write('from utils import *\r\n')
            f.write('from webduino.config import *\r\n')
            f.write('cfg = Config.load()\r\n')
            f.write("do_connect(cfg['ssid1'] , cfg['passwd1'])\r\n")
            f.write("Utils.save('"+url+"','"+file+"')\r\n")
            f.close()
            self.report('save')
            time.sleep(1)
            machine.reset()

        else:
            try:
                cmd = dataArgs.pop(0)
                Board.extraCmd(cmd,dataArgs)
            except Exception as e:
                debug.print("Board extraCmd error:"+e)
                pass