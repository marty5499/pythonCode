import dht , machine

dht11 = dht.DHT11(machine.Pin(0))
dht11.measure()
temp = dht11.temperature() # eg. 23 (°C)
humi = dht11.humidity()
print("temp:%s , humi:%s"%(temp,humi))

