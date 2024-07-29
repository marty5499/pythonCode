# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine
#uos.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()

# 5c:cf:7f:68:e2:ce
# b'\x5c\xcf\x7f\x68\xe2\xce'
from webduino.espnow_8266 import ESPNow
e = ESPNow()

