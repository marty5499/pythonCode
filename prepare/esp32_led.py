import machine
import time

# LILYGO state LED: pin2

def getLED(i):
    return machine.Pin(i, machine.Pin.OUT)