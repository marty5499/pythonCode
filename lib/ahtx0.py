# The MIT License (MIT)
#
# Copyright (c) 2020 Kattni Rembor for Adafruit Industries
# Copyright (c) 2020 Andreas Bühl
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
MicroPython driver for the AHT10 and AHT20 Humidity and Temperature Sensor
Author(s): Andreas Bühl, Kattni Rembor
"""

import utime
from micropython import const


class AHT10:
    """Interface library for AHT10/AHT20 temperature+humidity sensors"""

    AHTX0_I2CADDR_DEFAULT = const(0x38)  # Default I2C address
    AHTX0_CMD_INITIALIZE = 0xE1  # Initialization command
    AHTX0_CMD_TRIGGER = const(0xAC)  # Trigger reading command
    AHTX0_CMD_SOFTRESET = const(0xBA)  # Soft reset command
    AHTX0_STATUS_BUSY = const(0x80)  # Status bit for busy
    AHTX0_STATUS_CALIBRATED = const(0x08)  # Status bit for calibrated

    def __init__(self, i2c, address=AHTX0_I2CADDR_DEFAULT):
        utime.sleep_ms(20)  # 20ms delay to wake up
        self._i2c = i2c
        self._addres = address
        self._buf = bytearray(6)
        self.reset()
        if not sel
