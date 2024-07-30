# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

import time
from webduino.espnow import ESPNow


esp = ESPNow('wbitv1')
#esp = ESPNow()
esp.recv()

time.sleep(2)

