from machine import SPI, Pin
from driver import st7735_buf
from lib.easydisplay import EasyDisplay

class Display:
    def __init__(self, font, width=80, height=160, baudrate=40000000, polarity=0, phase=0,
                 sck_pin=5, mosi_pin=3, cs_pin=4, dc_pin=2, res_pin=1, bl_pin=37,
                 rotate=3, invert=False, rgb=True, color=0xFFFF, clear=True):
        self.spi = SPI(2, baudrate=baudrate, polarity=polarity, phase=phase, sck=Pin(sck_pin), mosi=Pin(mosi_pin))
        self.dp = st7735_buf.ST7735(
            width=width, height=height, spi=self.spi,
            cs=Pin(cs_pin), dc=Pin(dc_pin), res=Pin(res_pin),
            rotate=rotate, bl=Pin(bl_pin), invert=invert, rgb=rgb
        )
        self.ed = EasyDisplay(self.dp, "RGB565", font=font, show=True)
        self.color = color
        self.clear_screen = clear
        if clear:
            self.ed.clear()

    def rect(self, x, y, w, h, color):
        self.ed.rect(x, y, w, h, color)

    def text(self, text, x, y, color=None, clear=None):
        if color is None:
            color = self.color
        if clear is None:
            clear = self.clear_screen
        self.ed.text(text, x, y, color=color, clear=clear)

    def clear(self):
        self.ed.clear()
