import network, ubinascii
from umqtt.simple import MQTTClient
from webduino.debug import debug
import machine

class MQTT:
    
    def connect(user ='webduino' ,pwd='webduino'):
        MQTT.now = 0
        MQTT.user = user
        MQTT.pwd = pwd
        mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode().replace(':','')
        MQTT.client = MQTTClient('wa'+mac, MQTT.server, user=user, password=pwd)
        print("set last_will...")
        MQTT.set_last_will(MQTT.topic_report, MQTT.topic_report_msg)
        state = True if MQTT.client.connect() == 0 else False
        try:
            debug.print("resubscribe:",MQTT.subTopic)
            MQTT.sub(MQTT.subTopic,MQTT.callback)
        except:
            pass
        return state
        
    def pub(topic,msg):
        MQTT.client.publish(topic,msg)

    def sub(topic,cb):
        MQTT.subTopic = topic
        MQTT.callback = cb
        MQTT.client.set_callback(cb)
        MQTT.client.subscribe(topic)
        debug.print("sub topic: %s"%topic)
        
    def set_last_will(topic, msg, retain=True, qos=1):
        MQTT.client.set_last_will(topic, msg, retain, qos)

    def checkMsg():
        try:
            MQTT.client.check_msg()
            MQTT.now += 1 
            if MQTT.now % 60 == 0:
                debug.print("MQTT ping")
                MQTT.now = 0
                MQTT.client.ping()
        except Exception as e:
            print("MQTT checkMsg Err:",e)
            #debug.print("MQTT broken !")
            machine.reset()