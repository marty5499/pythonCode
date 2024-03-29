import paho.mqtt.client as mqtt

MQTT_TOPIC1 = "my/topic" 

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    payload = 'MQTT測試成功！'
    client.publish(MQTT_TOPIC1, payload, qos=1)    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(username="kebbimqtt",password="IoeoK2hK5Wti")
#client.username_pw_set(username=“webduinomqtt”,password=“ItiK5oeoK2hW”)
client.connect("mqtt1.webduino.io", 1883, 60)
client.loop_forever()