###### tags: `micropython`
RGBLED
======


![](/uploads/upload_b4d0213294faef2e2191c653c12c5fce.png =50%x)


```python=
from machine import Pin
import time

p0 = Pin(0, Pin.OUT)
for i in range(10):
    time.sleep(0.25)
    p0.value(i%2)
```
