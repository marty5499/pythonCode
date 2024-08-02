import time
import espnow
from machine import SPI, Pin
from driver import st7735_buf
from lib.easydisplay import EasyDisplay

# ESP32S3 & ST7735
spi = SPI(2, baudrate=40000000, polarity=0, phase=0, sck=Pin(5), mosi=Pin(3))
dp = st7735_buf.ST7735(
    width=80,
    height=160,
    spi=spi,
    cs=Pin(4),    # TFT_CS_PIN
    dc=Pin(2),    # TFT_DC_PIN
    res=Pin(1),   # TFT_RES_PIN
    rotate=3,
    bl=Pin(37),   # TFT_LED_PIN
    invert=True,
    rgb=False
)
ed = EasyDisplay(dp, "RGB565", font="/text_lite_16px_2312.v3.bmf", show=True, color=0xFFFF, clear=True)

while True:
    ed.bmp("/pic01.bmp", 0, 0)
    time.sleep(2)
    ed.bmp("/pic02.bmp", 0, 0)
    ed.text("你好! Webduino", 0, 0,clear=False)
    time.sleep(2)

