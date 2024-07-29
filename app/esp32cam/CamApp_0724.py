from webduino.board import Board
from webduino.config import JSONFile
from webduino.led import LED
from webduino.debug import debug
from webduino.camera import Camera

from machine import WDT
import time, machine, urequests, gc, os, ubinascii, network

class CamApp():

    def getDefaultCfg():
        data = {}
        data['sendTime'] = 5
        data['enableCron'] = False 
        data['folderId'] = '1RPexLz2YOE2IzTYsYh-POMSKBHPZntcd'
        data['scriptId'] = 'AKfycbxboaMHyj3CRSHTDncHI2GXdUUbJfmbUXPmeGV8PsTOsikZHInkU_4ftVFMMs_G9Hk'
        return data
    
    def init(ledPin=4):
        debug.on()
        CamApp.cfg = JSONFile('webeye.cfg',CamApp.getDefaultCfg())
        ##
        CamApp.sendTime = CamApp.cfg.get('sendTime')
        CamApp.enableCron = CamApp.cfg.get('enableCron')
        ##
        #CamApp.wdt = WDT(timeout=3*60*1000)
        CamApp.snaping = False
        CamApp.led = LED(ledPin)
        CamApp.led.blink(0.5)
        print("init board...")
        CamApp.board = Board()
        print("cam init...")
        CamApp.cam = Camera
        CamApp.cam.resolution = CamApp.board.config.data['resolution']
        CamApp.cam.init()
        CamApp.devId = CamApp.board.devId
        CamApp.devSSID = CamApp.board.config.data['devSSID']
        CamApp.stream = 0
        # ["Disable", "Real-time", "1 second", "3 seconds", "5 seconds", "10 seconds", "15 seconds", "30 seconds", "60 seconds"]
        stream = int(CamApp.board.config.data['stream'])
        if (stream == 1):
            CamApp.stream = 0.2
        elif (stream == 2):
            CamApp.stream = 1
        elif (stream == 3):
            CamApp.stream = 3
        elif (stream == 4):
            CamApp.stream = 5
        elif (stream == 5):
            CamApp.stream = 10
        elif (stream == 6):
            CamApp.stream = 15
        elif (stream == 7):
            CamApp.stream = 30
        elif (stream == 8):
            CamApp.stream = 60
        print('stream setting:'+str(CamApp.stream))
        CamApp.reg_cmd()
        #CamApp.board.setExtraCmdProcess(CamApp.camCmd)
        CamApp.board.publish(CamApp.devId+'/state', 'ready '+str(CamApp.cfg.data))
        #print("set RTC...")
        #CamApp.setRTC()
        CamApp.led.blink(0)
        gc.collect()

    def reg_cmd():
        CamApp.board.onTopic("reboot",CamApp.cmd_reboot)
        CamApp.board.onTopic("clear",CamApp.cmd_clear)
        CamApp.board.onTopic("state",CamApp.cmd_state)
        CamApp.board.onTopic("led",CamApp.cmd_led)
        CamApp.board.onTopic("info",CamApp.cmd_info)
        CamApp.board.onTopic("sendTime",CamApp.cmd_sendTime)
        CamApp.board.onTopic("snapshot",CamApp.cmd_snapshot)
        CamApp.board.onTopic("capture",CamApp.cmd_capture)
        CamApp.board.onTopic("enableCron",CamApp.cmd_enableCron)

    #重新開機
    def cmd_reboot(args):
        print("cmd_reboot")
        CamApp.board.publish(CamApp.devId+'/state', 'reboot')
        time.sleep(1)
        machine.reset()        

    # 清除參數
    def cmd_clear(args):
        print("cmd_clear")
        os.remove(CamApp.cfg.filename)
        CamApp.board.publish(CamApp.devId+'/state', 'setOK clear')
    
    # 狀態查詢
    def cmd_state(args):
        print("cmd_state:"+args)
        if(args=='ping'):
            CamApp.board.publish(CamApp.devId+'/state', 'pong')
        if(args=='time'):
            CamApp.board.publish(CamApp.devId+'/state', CamApp.getTime())

    # 補光燈
    def cmd_led(args):
        print("cmd_led:"+args)
        try:
            CamApp.led.on(int(args))
        except:
            CamApp.led.on(1000)

    # 取得資訊 info
    def cmd_info(args):
        print("cmd_info")
        CamApp.board.publish(CamApp.devId+'/state', 'info '+str(CamApp.cfg.data))
    
    # 間隔時間 sendTime
    def cmd_sendTime(args):
        print("cmd_sendTime:"+args)
        CamApp.sendTime = int(args)
        CamApp.cfg.put('sendTime',CamApp.sendTime)
        CamApp.cfg.save()
        CamApp.board.publish(CamApp.devId+'/state', 'setOK sendTime')    

    # 拍照 snapshot
    def cmd_snapshot(args):
        print("cmd_snapshot")
        CamApp.snapshot_upload('snap-')
        
    # 拍照 capture
    def cmd_capture(args):
        print("cmd_capture")
        CamApp.snaping = True
        CamApp.board.publish((CamApp.devId+'/state'), 'waiting')
        try:
            img = CamApp.cam.capture()
            img = CamApp.cam.capture()
            CamApp.board.publish((CamApp.devId+'/state'), 'uploading')
            filename = 'capture-%s.jpg' % CamApp.getTime(timeType=1)
            print("filename:%s" %  filename)
            FileBrowser.upload(img,'/%s/%s' % (args,filename) )
            print("upload done.")
            CamApp.board.publish((CamApp.devId+'/state'), 'upload %s' % filename)
            CamApp.snaping = False
            #print("capture ok")
        except Exception as e:
            print(e)
            print('')
            CamApp.board.publish((CamApp.devId+'/state'), 'except camera failure,reboot !')
            time.sleep(1)
            machine.reset()
        
        
    # 攝影開關 enableCron
    def cmd_enableCron(args):
        print("cmd_enableCron:"+args)
        CamApp.enableCron = bool(args.replace('False',''))
        CamApp.cfg.put('enableCron',CamApp.enableCron)
        CamApp.cfg.save()
        CamApp.board.publish(CamApp.devId+'/state', 'setOK enableCron')
        CamApp.now = 0
            
    def setRTC():
        print("set ntptime & rtc")
        ntptime.NTP_DELTA = ntptime.NTP_DELTA - 8*60*60
        setNTPTime = False
        while(not setNTPTime):
            try:
                ntptime.settime()
                setNTPTime = True
            except Exception as e:
                print("ntptime error !")
                print(e)
        CamApp.rtc = machine.RTC()

    def getTime(timeType=0):
        _time = CamApp.rtc.datetime()
        MM =  _time[1]
        dd =  _time[2]
        hh =  _time[4]
        mm =  _time[5]
        ss =  _time[6]
        MM = "0"+str(MM) if MM < 10 else str(MM)
        dd = "0"+str(dd) if dd < 10 else str(dd)
        hh = "0"+str(hh) if hh < 10 else str(hh)
        mm = "0"+str(mm) if mm < 10 else str(mm)
        ss = "0"+str(ss) if ss < 10 else str(ss)
        if(timeType==0):
            return MM+"/"+dd+" "+hh+":"+mm+":"+ss
        else:
            return MM+dd+"-"+hh+mm+ss

    def run(enableCron=True,enableDeepSleepMode=0):
        cnt = 0 
        print("run...")
        while True and CamApp.stream != 0:
            try:
                CamApp.board.check()
                # https://flows.webduino.io/api/view/cam03
                CamApp.board.publish(('webeye/stream/'+CamApp.devSSID), CamApp.cam.capture())
                print(str(cnt)+"["+ str(CamApp.stream)+('] webeye/stream/'+CamApp.devSSID), gc.mem_free())
                time.sleep(0.1 + CamApp.stream)
                cnt = cnt + 1
                #直接重新開機
                #machine.reset()
            except Exception as e:
                CamApp.snaping = False
                print("CamApp exception:",e)
                CamApp.board.wifi.checkConnection('')


#####################
try:
    import cmd
    machine.reset()
except:
    pass
#####################
try:
    CamApp.init(ledPin=4)
    CamApp.board.wifi.web.cam = CamApp.cam # embedded cam to webserver
    CamApp.run(enableCron = True , enableDeepSleepMode = 0) # 0 min: do not deepsleep
except Exception as e:
    print(e)
    print('')
    machine.reset()