from TM1637 import TM1637
from machine import Pin
tm = TM1637(clk=Pin(0), dio=Pin(2))
tm.show('1234', False)  # ':' True | False
