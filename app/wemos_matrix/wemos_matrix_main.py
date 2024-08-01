import time, espnow, time, ubinascii, network, machine
import uwemosledmatrix
from machine import Pin


def callback(peer,msg):
    print(msg)

#uwemosledmatrix.text('1')
uwemosledmatrix.scroll('1234567890',50)
esp.recv(callback)

while True:
    esp.irecv(1)
