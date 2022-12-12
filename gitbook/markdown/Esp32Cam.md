###### tags: `micropython`
Esp32Cam
====
> [[回首頁]](https://md.kingkit.codes/cYuxdDkOSJ2guIzPG-KHqA?view)

![](/uploads/upload_613552a6581a20069bbb7f60dfd4aa2e.png)


### [Jupyter 範例程式](https://webbit-jupyter.webduino.io/notebooks/ESP32-Cam%20%E7%AF%84%E4%BE%8B.ipynb)


### 不用SD可使用腳位
測試可用 Pin13 , Pin15 , Pin14 , Pin02

```python=
# PWM 使用範例
from machine import Pin, PWM
p13 = Pin(2, Pin.OUT)
p15 = Pin(14, Pin.OUT)
pwm13 = PWM(p13, freq=1000, duty=500)
p13.value(0)
p15.value(0)
```

### 內建一顆LED燈 GPIO33
![](/uploads/upload_ebaba600efb4e1d24ee751bf582bcdcc.png =50%x)

## MicroSD 使用腳位
The following pins are used to interface with the microSD card when it is on operation.


| MicroSD            |   ESP32 | 可用 |
|:------------------ | -------:| ----:|
| CLK                |  GPIO14 |    ✔ |
| CMD                | GPIO 15 |    ✔ |
| DATA0              |  GPIO 2 |    ✔ |
| DATA1 / flashlight |  GPIO 4 |      |
| DATA2              | GPIO 12 |      |
| DATA3              | GPIO 13 |    ✔ |

| 其他腳位  |   ESP32 | 可用 |
|:--------- | -------:| ----:|
| Uart0 TXD |  GPIO 1 |    ✔ |
| Uart0 RXD |  GPIO 3 |    ✔ |
| Uart2 RXD | GPIO 16 |    ✔ |


## 鏡頭

X-JM0007A 廣角鏡頭
![](/uploads/upload_c9d99f62e9f5bc3fc87226496ab3d8bd.png)

X-JM0008B 魚眼鏡頭
![](/uploads/upload_8a2748cbd0b43302575d945729da2548.png)

## Touch Enable
There are ten capacitive touch-enabled pins that can be used on the ESP32: 
0, 2, 4, 12, 13 14, 15, 27, 32, 33

## ADC
- ADC1:
    - 8 channels: GPIO32 - GPIO39

- ADC2:
    - 10 channels: GPIO0, GPIO2, GPIO4, GPIO12 - GPIO15, GOIO25 - GPIO27

## 編譯 esp32-cam 韌體 (esp-idf v4.2)

### 1.準備好相關套件與環境設定
```console=
mdir ~/esp32-mpy
cd ~/esp32-mpy

# clone micropython repo
git clone https://github.com/micropython/micropython.git

# clone 開發者 lemariva's repo
git clone https://github.com/lemariva/micropython-camera-driver

# 使用 Docker's esp-idf 環境，掛入當下 micropython 目錄
docker run --rm -v $PWD:/project -w /project -it espressif/idf:release-v4.2

# 到 esp-idf 元件目錄下，新增 esp32-cam 元件
cd /opt/esp/idf/components
git clone https://github.com/espressif/esp32-camera

# 切換到這個點，這是試過可以編譯成功的點
cd esp32-camera
git checkout 221d24da1901b6aee8df6c1a1160ad02faa685b5
# 新版本
git checkout 093688e0b3521ac982bc3d38bbf92059d97e3613

# COPY esp32cam 開發板建置參數的相關目錄
cd /project/micropython/ports/esp32
cp -R ../../../micropython-camera-driver/boards/* /project/micropython/ports/esp32/boards/
```

:::danger
最特殊的一步，修改 main.c，找到關鍵字進行註解
:::
```c=
main.c: modify the lines inside the #if CONFIG_ESP32_SPIRAM_SUPPORT || CONFIG_SPIRAM_SUPPORT, they should look like:
    /*
    // Try to use the entire external SPIRAM directly for the heap
    size_t mp_task_heap_size;
    void *mp_task_heap = (void *)SOC_EXTRAM_DATA_LOW;
    switch (esp_spiram_get_chip_size()) {
        case ESP_SPIRAM_SIZE_16MBITS:
            mp_task_heap_size = 2 * 1024 * 1024;
            break;
        case ESP_SPIRAM_SIZE_32MBITS:
        case ESP_SPIRAM_SIZE_64MBITS:
            mp_task_heap_size = 4 * 1024 * 1024;
            break;
        default:
            // No SPIRAM, fallback to normal allocation
            mp_task_heap_size = heap_caps_get_largest_free_block(MALLOC_CAP_8BIT);
            mp_task_heap = malloc(mp_task_heap_size);
            break;
    }
    */
    size_t mp_task_heap_size;
    mp_task_heap_size = 2 * 1024 * 1024;
    void *mp_task_heap = malloc(mp_task_heap_size);
    ESP_LOGI("main", "Allocated %dK for micropython heap at %p", mp_task_heap_size/1024, mp_task_heap);
```

### 2.編譯 esp32Cam 韌體

```console=
# 然後到 micropython 目錄建置 cross
cd /project/micropython
make -C mpy-cross


# 終於可以編譯 ESP32CAM 韌體了
cd /project/micropython/ports/esp32

make USER_C_MODULES=../../../../micropython-camera-driver/src/micropython.cmake  BOARD=GENERIC_CAM all

# 新版本改用 ESP32_CAM
make USER_C_MODULES=../../../../micropython-camera-driver/src/micropython.cmake BOARD=ESP32_CAM all

```

### 3.燒錄 esp32Cam 韌體 (使用 esptool.py 燒錄)
:::danger
燒錄不在容器內，並且需使用conda切換運行環境
conda activate esp32
:::

```console=
## 進入產生韌體的目錄
cd ~/esp32-mpy/micropython/ports/esp32/build-GENERIC_CAM

## erase flash
esptool.py -p /dev/cu.usbserial-1440 erase_flash

## 燒錄韌體
esptool.py -b 230400 -p /dev/cu.usbserial-1440 write_flash 0x8000 partition_table/partition-table.bin 0x1000 bootloader/bootloader.bin 0x10000 micropython.bin
```


### 很多 esp32Cam 範例
https://randomnerdtutorials.com/projects-esp32-cam/

### 寫照片到檔案中
https://www.bilibili.com/read/cv8818646



## Google Script App 檔案上傳的腳本
```javascript=
// queryString 就是 e.parameters
// req: https://script.google.com/script/exec?filename=ok.jpg&folderId=asdklfn4ou83n
// res: {"id":"123456789" , "name":"ok.jpg" , "size":77656}

function doPost(e) {
 var strAux = e.parameter.data;
 var strInput = strAux.replace(/ /g, "+");
 var folderId = e.parameters.folderId;
 var decoded = Utilities.base64Decode(strInput, Utilities.Charset.UTF_8);
 var blob = Utilities.newBlob(decoded , MimeType.JPEG, e.parameters.filename);
 var file = DriveApp.getFolderById(folderId).createFile(blob);
 var fileObj = {
   'id':file.getId(),
   'name':file.getName(),
   'size':file.getSize()
 }
 return ContentService.createTextOutput(JSON.stringify(fileObj)).setMimeType(ContentService.MimeType.JSON);
}
```

## 檔案上傳的 mpy 程式碼
:::info
上傳到這 [目錄](https://drive.google.com/drive/u/0/folders/1oaJx5OUOK8FekcANGgr972thFjm-AFrv)
:::
```python=
import network
from machine import Pin, Timer, I2C, ADC
import camera
import machine
import time
import uasyncio as asyncio
import ubinascii
import gc
import usocket
import json
import urequests

def do_connect():
    global connected
    sta_if = network.WLAN(network.STA_IF)
    if(not sta_if.isconnected()):
        sta_if.active(True)
        sta_if.connect('KingKit_2.4G', 'webduino')
        cnt = 0
        while not sta_if.isconnected():
            cnt = cnt + 1
            time.sleep(0.5)
            if cnt == 12:
                break
    print('network config:', sta_if.ifconfig())

    
def cameraInit():
    camera.init(0, format=camera.JPEG,xclk_freq=camera.XCLK_20MHz)
    camera.framesize(15)
    camera.quality(10)
    camera.framesize(camera.FRAME_XGA)
    time.sleep(0.1)
    
def snapshot():
    jpg = camera.capture()
    image = ubinascii.b2a_base64(jpg)
    del jpg
    time.sleep(0.1)
    gc.collect()
    return image
    
    
def upload(image,idx):
    myScriptID = 'AKfycbxsmXppkOGdGNftGKSXrWJcFTr8qOI5iior8KNMnNY7ebq4SO6ATKASPgMdFFINYKnNcw'
    url = 'https://script.google.com/macros/s/'+myScriptID+'/exec'
    myFilename = "filename="+str(idx)+".jpg&mimetype=image/jpeg&data="
    myDomain = "script.google.com"

    data = myFilename + image.decode()
    method = "POST"
    try:
        proto, dummy, host, path = url.split("/", 3)
    except ValueError:
        proto, dummy, host = url.split("/", 2)
        path = ""
    if proto == "http:":
        port = 80
    elif proto == "https:":
        import ussl
        port = 443
    else:
        raise ValueError("Unsupported protocol: " + proto)
    if ":" in host:
        host, port = host.split(":", 1)
        port = int(port)

    ai = usocket.getaddrinfo(host, port, 0, usocket.SOCK_STREAM)
    ai = ai[0]
    s = usocket.socket(ai[0], ai[1], ai[2])
    s.connect(ai[-1])
    if proto == "https:":
        s = ussl.wrap_socket(s, server_hostname=host)
    s.write(b"%s /%s HTTP/1.0\r\n" % (method, path))
    s.write(b"Host: %s\r\n" % host)
    s.write(b"Content-Length: %d\r\n" % len(data))
    s.write(b"Content-Type: application/x-www-form-urlencoded\r\n")
    s.write(b"\r\n")
    s.write(data)
    # response
    l = s.readline()
    l = l.split(None, 2)
    status = int(l[1])
    reason = ""
    if len(l) > 2:
        reason = l[2].rstrip()
    while True:
        l = s.readline()
        if not l or l == b"\r\n":
            break
        if l.startswith(b"Transfer-Encoding:"):
            if b"chunked" in l:
                raise ValueError("Unsupported " + l)
    
    
print("connecting...")
do_connect()

print("init camera...")
cameraInit()

idx = 0
while True:
    idx = ++idx
    print("snapshot..."+str(idx))
    image = snapshot()
    print("upload...")
    upload(image,idx)
print("done.")
```

## main.c
```c=
/*
 * This file is part of the MicroPython project, http://micropython.org/
 *
 * Development of the code in this file was sponsored by Microbric Pty Ltd
 *
 * The MIT License (MIT)
 *
 * Copyright (c) 2016 Damien P. George
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */

#include <stdio.h>
#include <string.h>
#include <stdarg.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "nvs_flash.h"
#include "esp_task.h"
#include "soc/cpu.h"
#include "esp_log.h"

#if CONFIG_IDF_TARGET_ESP32
#include "esp32/spiram.h"
#elif CONFIG_IDF_TARGET_ESP32S2
#include "esp32s2/spiram.h"
#elif CONFIG_IDF_TARGET_ESP32S3
#include "esp32s3/spiram.h"
#endif

#include "py/stackctrl.h"
#include "py/nlr.h"
#include "py/compile.h"
#include "py/runtime.h"
#include "py/persistentcode.h"
#include "py/repl.h"
#include "py/gc.h"
#include "py/mphal.h"
#include "shared/readline/readline.h"
#include "shared/runtime/pyexec.h"
#include "uart.h"
#include "usb.h"
#include "usb_serial_jtag.h"
#include "modmachine.h"
#include "modnetwork.h"
#include "mpthreadport.h"

#if MICROPY_BLUETOOTH_NIMBLE
#include "extmod/modbluetooth.h"
#endif

// MicroPython runs as a task under FreeRTOS
#define MP_TASK_PRIORITY        (ESP_TASK_PRIO_MIN + 1)
#define MP_TASK_STACK_SIZE      (16 * 1024)

// Set the margin for detecting stack overflow, depending on the CPU architecture.
#if CONFIG_IDF_TARGET_ESP32C3
#define MP_TASK_STACK_LIMIT_MARGIN (2048)
#else
#define MP_TASK_STACK_LIMIT_MARGIN (1024)
#endif

int vprintf_null(const char *format, va_list ap) {
    // do nothing: this is used as a log target during raw repl mode
    return 0;
}

void mp_task(void *pvParameter) {
    volatile uint32_t sp = (uint32_t)get_sp();
    #if MICROPY_PY_THREAD
    mp_thread_init(pxTaskGetStackStart(NULL), MP_TASK_STACK_SIZE / sizeof(uintptr_t));
    #endif
    #if CONFIG_USB_ENABLED
    usb_init();
    #elif CONFIG_ESP_CONSOLE_USB_SERIAL_JTAG
    usb_serial_jtag_init();
    #else
    uart_init();
    #endif
    machine_init();

    // TODO: CONFIG_SPIRAM_SUPPORT is for 3.3 compatibility, remove after move to 4.0.
    #if CONFIG_ESP32_SPIRAM_SUPPORT || CONFIG_SPIRAM_SUPPORT
    /*
    // Try to use the entire external SPIRAM directly for the heap
    size_t mp_task_heap_size;
    void *mp_task_heap = (void *)SOC_EXTRAM_DATA_LOW;
    switch (esp_spiram_get_chip_size()) {
        case ESP_SPIRAM_SIZE_16MBITS:
            mp_task_heap_size = 2 * 1024 * 1024;
            break;
        case ESP_SPIRAM_SIZE_32MBITS:
        case ESP_SPIRAM_SIZE_64MBITS:
            mp_task_heap_size = 4 * 1024 * 1024;
            break;
        default:
            // No SPIRAM, fallback to normal allocation
            mp_task_heap_size = heap_caps_get_largest_free_block(MALLOC_CAP_8BIT);
            mp_task_heap = malloc(mp_task_heap_size);
            break;
    }
    */
    size_t mp_task_heap_size;
    mp_task_heap_size = 2 * 1024 * 1024;
    void *mp_task_heap = malloc(mp_task_heap_size);
    ESP_LOGI("main", "Allocated %dK for micropython heap at %p", mp_task_heap_size/1024, mp_task_heap);

    #elif CONFIG_ESP32S2_SPIRAM_SUPPORT || CONFIG_ESP32S3_SPIRAM_SUPPORT
    // Try to use the entire external SPIRAM directly for the heap
    size_t mp_task_heap_size;
    size_t esp_spiram_size = esp_spiram_get_size();
    void *mp_task_heap = (void *)SOC_EXTRAM_DATA_HIGH - esp_spiram_size;
    if (esp_spiram_size > 0) {
        mp_task_heap_size = esp_spiram_size;
    } else {
        // No SPIRAM, fallback to normal allocation
        mp_task_heap_size = heap_caps_get_largest_free_block(MALLOC_CAP_8BIT);
        mp_task_heap = malloc(mp_task_heap_size);
    }
    #else
    // Allocate the uPy heap using malloc and get the largest available region
    size_t mp_task_heap_size = heap_caps_get_largest_free_block(MALLOC_CAP_8BIT);
    void *mp_task_heap = malloc(mp_task_heap_size);
    #endif

soft_reset:
    // initialise the stack pointer for the main thread
    mp_stack_set_top((void *)sp);
    mp_stack_set_limit(MP_TASK_STACK_SIZE - MP_TASK_STACK_LIMIT_MARGIN);
    gc_init(mp_task_heap, mp_task_heap + mp_task_heap_size);
    mp_init();
    mp_obj_list_append(mp_sys_path, MP_OBJ_NEW_QSTR(MP_QSTR__slash_lib));
    readline_init0();

    // initialise peripherals
    machine_pins_init();
    #if MICROPY_PY_MACHINE_I2S
    machine_i2s_init0();
    #endif

    // run boot-up scripts
    pyexec_frozen_module("_boot.py");
    pyexec_file_if_exists("boot.py");
    if (pyexec_mode_kind == PYEXEC_MODE_FRIENDLY_REPL) {
        int ret = pyexec_file_if_exists("main.py");
        if (ret & PYEXEC_FORCED_EXIT) {
            goto soft_reset_exit;
        }
    }

    for (;;) {
        if (pyexec_mode_kind == PYEXEC_MODE_RAW_REPL) {
            vprintf_like_t vprintf_log = esp_log_set_vprintf(vprintf_null);
            if (pyexec_raw_repl() != 0) {
                break;
            }
            esp_log_set_vprintf(vprintf_log);
        } else {
            if (pyexec_friendly_repl() != 0) {
                break;
            }
        }
    }

soft_reset_exit:

    #if MICROPY_BLUETOOTH_NIMBLE
    mp_bluetooth_deinit();
    #endif

    machine_timer_deinit_all();

    #if MICROPY_PY_THREAD
    mp_thread_deinit();
    #endif

    gc_sweep_all();

    mp_hal_stdout_tx_str("MPY: soft reboot\r\n");

    // deinitialise peripherals
    machine_pwm_deinit_all();
    // TODO: machine_rmt_deinit_all();
    machine_pins_deinit();
    machine_deinit();
    usocket_events_deinit();

    mp_deinit();
    fflush(stdout);
    goto soft_reset;
}

void boardctrl_startup(void) {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        nvs_flash_erase();
        nvs_flash_init();
    }
}

void app_main(void) {
    // Hook for a board to run code at start up.
    // This defaults to initialising NVS.
    MICROPY_BOARD_STARTUP();

    // Create and transfer control to the MicroPython task.
    xTaskCreatePinnedToCore(mp_task, "mp_task", MP_TASK_STACK_SIZE / sizeof(StackType_t), NULL, MP_TASK_PRIORITY, &mp_main_task_handle, MP_TASK_COREID);
}

void nlr_jump_fail(void *val) {
    printf("NLR jump failed, val=%p\n", val);
    esp_restart();
}

// modussl_mbedtls uses this function but it's not enabled in ESP IDF
void mbedtls_debug_set_threshold(int threshold) {
    (void)threshold;
}

void *esp_native_code_commit(void *buf, size_t len, void *reloc) {
    len = (len + 3) & ~3;
    uint32_t *p = heap_caps_malloc(len, MALLOC_CAP_EXEC);
    if (p == NULL) {
        m_malloc_fail(len);
    }
    if (reloc) {
        mp_native_relocate(reloc, buf, (uintptr_t)p);
    }
    memcpy(p, buf, len);
    return p;
}
```



```
import camera
#引入camera库
camera.init(0, format=camera.JPEG)  
#初始化相机


设置分辨率（不设置分辨率默认是200万像素）
camera.framesize(camera.FRAME_240X240)

分辨率参数：
camera.FRAME_96X96   96x96
camera.FRAME_240X240   240x240
camera.FRAME_QVGA    320X240
camera.FRAME_VGA   640x480
camera.FRAME_SVGA    800x600
camera.FRAME_HD     1280X720
 

设置特殊模式

# specialeffects
camera.speffect(camera.EFFECT_NONE)
# The optionsare the following:
# EFFECT_NONE(default) EFFECT_NEG EFFECT_BW EFFECT_RED EFFECT_GREEN EFFECT_BLUE EFFECT_RETRO

参数
EFFECT_NEG 偏紫色

BW 黑白
RED 红
GEEN 绿
Blue 蓝
RETRO 怀旧风格

 

#设置白平衡
# white balance
camera.whitebalance(camera.WB_NONE)
# The optionsare the following:
# WB_NONE(default) WB_SUNNY WB_CLOUDY WB_OFFICE WB_HOME

 

#设置饱和度
# saturation
camera.saturation(0)
# -2,2 (default0). -2 grayscale

 

#设置亮度
# brightness
camera.brightness(0)
# -2,2 (default0). 2 brightness


#设置对比度
# contrast
camera.contrast(0)
#-2,2 (default0). 2 highcontrast


#设置图片质量
# quality
camera.quality(10)
# 10-63 lowernumber means higher quality
 

所有设置必须在camera.capture()执行之前。

#拍照
buf = camera.capture()
img=open("a.jpg","w")
img.write(img)
img.close()

 

#SD卡挂载
import uos
from machine import SDCard
uos.mount(SDCard(),'/sd')

#挂载在SD卡上了
uos.chdir('sd') #切换到sd卡目录
uos.listdir() #查看文件下所有的文件 作者：邪恶的胖次菌 https://www.bilibili.com/read/cv8818646 出处：bilibili
```




```
object <module 'camera'> is of type module
  __name__ -- camera
  init -- <function>
  deinit -- <function>
  capture -- <function>
  flip -- <function>
  mirror -- <function>
  framesize -- <function>
  quality -- <function>
  contrast -- <function>
  saturation -- <function>
  brightness -- <function>
  speffect -- <function>
  whitebalance -- <function>
  JPEG -- 3
  YUV422 -- 1
  GRAYSCALE -- 2
  RGB565 -- 0
  FRAME_96X96 -- 0
  FRAME_QQVGA -- 1
  FRAME_QCIF -- 2
  FRAME_HQVGA -- 3
  FRAME_240X240 -- 4
  FRAME_QVGA -- 5
  FRAME_CIF -- 6
  FRAME_HVGA -- 7
  FRAME_VGA -- 8
  FRAME_SVGA -- 9
  FRAME_XGA -- 10
  FRAME_HD -- 11
  FRAME_SXGA -- 12
  FRAME_UXGA -- 13
  FRAME_FHD -- 14
  FRAME_P_HD -- 15
  FRAME_P_3MP -- 16
  FRAME_QXGA -- 17
  FRAME_QHD -- 18
  FRAME_WQXGA -- 19
  FRAME_P_FHD -- 20
  FRAME_QSXGA -- 21
  FRAME_QSXGA -- 21
  WB_NONE -- 0
  WB_SUNNY -- 1
  WB_CLOUDY -- 2
  WB_OFFICE -- 3
  WB_HOME -- 4
  EFFECT_NONE -- 0
  EFFECT_NEG -- 1
  EFFECT_BW -- 2
  EFFECT_RED -- 3
  EFFECT_GREEN -- 4
  EFFECT_BLUE -- 5
  EFFECT_RETRO -- 6
  XCLK_10MHz -- 10000000
  XCLK_20MHz -- 20000000
  ```
