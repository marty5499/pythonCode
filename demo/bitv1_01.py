import time
from webduino.webbitv1 import WebBit  
wbit = WebBit()

list_do = [[262,0.25]] 
list_re = [[294,0.25]]
list_me = [[329,0.25]]

while True: 
   if wbit.btnA():  
       wbit.play(list_do + list_re + list_me)
   if wbit.btnB():  
       wbit.play(list_me + list_re+ list_do)
