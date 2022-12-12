###### tags: `micropython`
Jupyter
=======

## 1. 更新插件程式
最簡單方式，就是直接進入webai-jupyter容器修改程式
![](/uploads/upload_a3cab00ab343d7a1dea12f7a9fcfba11.png)

容器中插件程式位置
/usr/local/share/jupyter/nbextensions/repl/main.js
/usr/local/share/jupyter/nbextensions/repl/repl.js

修改後就可以直接測試，不用重新啟動 Server


## 2. 測試完成，重新 Build docker image
1. 在webai-jupyter目錄下，執行 ./build.sh
![](/uploads/upload_d3842714693b65c81509f2856fd97023.png)

2. push 新的images 到 docker.io
![](/uploads/upload_6711aff11e3890a499d1324e13c263ba.png)

3. 在 portainer 重拉 image
![](/uploads/upload_83ec036d00bb3bfcbd594085ce9042c3.png)



## 產生新的 image
docker build -t jupyter/webai .

## 執行 jupyter-webai
docker run --name jupyter-webai -d -v ${PWD}/work:/home/jovyan/— -p 8888:8888 jupyter/webai

## 進入 jupyter-webai container
docker run --name jupyter-webai -e GRANT_SUDO=yes --user root -it -v ${PWD}/work:/home/jovyan/— -p 8888:8888 jupyter/webai bash



### API
https://jupyter-notebook.readthedocs.io/en/stable/extending/frontend_extensions.html

## Jupyter Notebook 完整介紹、安裝及使用說明
https://medium.com/ai-for-k12/jupyter-notebook-%E5%AE%8C%E6%95%B4%E4%BB%8B%E7%B4%B9-%E5%AE%89%E8%A3%9D%E5%8F%8A%E4%BD%BF%E7%94%A8%E8%AA%AA%E6%98%8E-846b5432f044

## 好用插件
，Jupyter notebook extensions之相見恨晚
[打造coding舒適環境](https://ithelp.ithome.com.tw/articles/10212035）


## 擴充套件位置
/Users/username/anaconda3/envs/jupyterexperiments/lib/python3.7/site-packages/jupyter_contrib_nbextensions/nbextensions

## 文件參考
https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/install.html

![](/uploads/upload_02fa807b0de0c630f74889dd9c5f0c6e.png)

目前電腦的conda config
![](/uploads/upload_2f942736a81a7fd3ff48e09c3c6f3269.png)


#### Conda 使用參考
https://medium.com/%E6%95%B8%E6%93%9A%E4%B8%8D%E6%AD%A2-not-only-data/anaconda-anjupyter-54144e75318f

#### Jupyter notebook 插件開發
https://aneesha.medium.com/creating-a-jupyter-notebook-extension-part-1-31c72032cad

### 安裝位置
~/opt/anaconda3/envs/jupyterlab-ext/lib/python3.9/site-packages/notebook


### Tensorflow 學習
https://tf.wiki/zh_hant/appendix/jupyterlab.html

### 安裝自訂插件
jupyter nbextension install myext

#### 安裝路徑
```console=
⇒  jupyter nbextension install myext
Making directory: /usr/local/share/jupyter/nbextensions/myext/
Copying: /Users/marty/kingkit.codes/dvlp/notebook/myext/main.js 
-> 
/usr/local/share/jupyter/nbextensions/myext/main.js
```


### 啟動自訂插件
jupyter nbextension enable myext/main

### 查看擴充面板就可以看到
![](/uploads/upload_7cf5856f1cf3d0b93ed4f5f41ff079ec.png)


## 插件
repl.js
```js=
const generateESP32UploadCode = (file, pythonCode) => {
  code = `
pycode = """
${pythonCode}
"""
import machine
# write python code
with open('${file}', 'w') as f:
    f.write(pycode)
with open ('${file}', 'r') as f:
    content = f.read()
`;
  return code;
};

const generateUploadCode = (type, file, pythonCode) => {
  code = `
pycode = """
${pythonCode}
"""
from Maix import utils
from time import sleep
import gc, machine, ujson
# write python code
with open('${file}', 'w') as f:
    f.write(pycode)
sleep(0.5)
with open ('${file}', 'r') as f:
    content = f.read()
# save firmware type
romFlagAddressStart = 0x1FFFF
preFlag = int.from_bytes(utils.flash_read(romFlagAddressStart, 1), "big")
romFlag = 1 if "${type}" == "mini" else 0
if preFlag != romFlag:
    utils.flash_write(romFlagAddressStart, bytes([romFlag]))
deployCmd = '_DEPLOY/{"url":"local"}'
cfg.init()
cfg.put('cmd', deployCmd)
`;
  return code;
};


class DataTransformer {
  constructor() {
    this.container = '';
    this.decoder = new TextDecoder();
    this.readLine = true;
  }

  setReadLine() {
    this.readLine = true;
    this.readByteArray = false;
  }

  setReadByteArray(bytes) {
    this.readLine = false;
    this.readByteArray = true;
    this.readBytes = bytes;
    this.byteArray = new Uint8Array();
  }

  transform(chunk, controller) {
    if (this.readLine) {
      chunk = this.decoder.decode(chunk);
      this.container += chunk;
      const lines = this.container.split('\r\n');
      this.container = lines.pop();
      lines.forEach(line => controller.enqueue(line));
    }
    if (this.readByteArray) {
      this.byteArray = new Uint8Array([...this.byteArray, ...chunk]);
      var byteArrayLength = this.byteArray.length;
      if (byteArrayLength >= this.readBytes) {
        var rtnByteArray = new Uint8Array([...this.byteArray.slice(0, this.readBytes)]);
        this.byteArray = new Uint8Array(
          [this.byteArray.slice(this.readBytes, byteArrayLength - this.readBytes)]);
        controller.enqueue(rtnByteArray);
      }
    }
  }

  flush(controller) {
    controller.enqueue(this.container);
  }
}

class REPL {
  constructor() {
    this.encoder = new TextEncoder();
    this.decoder = new TextDecoder();
    this.callback = function () {}
  }

  addListener(callback) {
    this.callback = callback;
  }

  async usbConnect() {
    var self = this;
    this.running = false;
    const filter = { usbVendorId: 6790 };
    if (self.port == undefined) {
      self.port = await navigator.serial.requestPort({});
      await this.port.open({ baudRate: 115200, dateBits: 8, stopBits: 1, });
      this.writer = this.port.writable.getWriter();
      this.stream = new DataTransformer();
      this.reader = this.port.readable.
      pipeThrough(new TransformStream(this.stream)).getReader();
      self.port.ondisconnect = function () {
        console.log("disconnect port");
        self.port = null;
      }
    }
  }

  async restart(chip) {
    try {
      await this.port.setSignals({ dataTerminalReady: false });
      await new Promise((resolve) => setTimeout(resolve, 100));
      await this.port.setSignals({ dataTerminalReady: true });
      if (chip == 'esp32') {
        console.log("esp32 restart")
        await new Promise((resolve) => setTimeout(resolve, 500));
      } else {
        await new Promise((resolve) => setTimeout(resolve, 1700));
      }
    } catch (e) {
      this.port = undefined;
      await this.usbConnect();
      await this.restart(chip);
    }
  }

  async enter(chip) {
    console.log(">>> restart...", chip)
    await this.restart(chip);
    for (var i = 0; i < 3; i++) {
      await this.writer.write(Int8Array.from([0x03 /*interrupt*/ ]));
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
    await this.writer.write(Int8Array.from([0x04 /*exit*/ ]));
    //*
    await this.write('', function (data) {
      return { value: '', done: true }
    })
    //*/
    console.log("REPL ready!");
  }

  async write(code, cb) {
    if (this.running) {
      if(cb!=null)
      cb('running...');
      return "";
    }
    this.running = true;
    var boundry = "===" + Math.random() + "==";
    await this.writer.write(Int8Array.from([0x01 /*RAW paste mode*/ ]));

    await new Promise((resolve) => setTimeout(resolve, 5));
    await this.writer.write(this.encoder.encode("print('" + boundry + "')\r\n"));
    var codes = code.split('\n');
    for (var i = 0; i < codes.length; i++) {
      await new Promise((resolve) => setTimeout(resolve, 5));
      await this.writer.write(this.encoder.encode(codes[i] + "\n"));
    }
    await new Promise((resolve) => setTimeout(resolve, 5));
    await this.writer.write(this.encoder.encode("print('" + boundry + "')\r\n"));
    await new Promise((resolve) => setTimeout(resolve, 5));

    await this.writer.write(Int8Array.from([0x04 /*exit*/ ]));
    var startBoundry = false;
    var rtnObj = "" + code.length;
    while (true) {
      var { value, done } = await this.reader.read();
      if (this.stream.readLine) {
        if (done) {
          //console.log("end:",value);
          this.running = false;
          return rtnObj;
        } else if (value.indexOf(">raw REPL; CTRL-B to exit") > 0) {
          continue;
        } else if (value == ">OK" + boundry) {
          startBoundry = true;
          //console.log("startBoundry...",value);
          continue;
        } else if (value == boundry) {
          //console.log("endBoundry...",value);
          this.running = false;
          return rtnObj;
        } else if (startBoundry && cb != null) {
          //console.log("output...",value);
          var { value, done } = await cb(value);
          if (done) return value;
        }
      } else if (this.stream.readByteArray) {
        var { value, done } = await cb(value);
        if (done) {
          this.running = false;
          return value;
        }
      }
    }
  }

  async uploadFile(type, filename, pythonCode) {
    if (type == 'esp32') {
      pythonCode = generateESP32UploadCode(filename, pythonCode);
      pythonCode = pythonCode.replace("\\", "\\\\");
      var rtn = await this.write(pythonCode, function (value) {
        if (value.substring(0, 4) == 'save') {
          return { 'value': value, 'done': true };
        }
      });
      return rtn;
    } else {
      pythonCode = generateUploadCode(type /*std|mini*/ , filename, pythonCode);
      pythonCode = pythonCode.replace("\\", "\\\\");
      return await this.write(pythonCode, function (value) {
        if (value.substring(0, 4) == 'save') {
          return { 'value': value, 'done': true };
        }
      });
    }
  }

  async setWiFi(pythonCode, ssid, pwd) {
    pythonCode += "cfg.init()\n";
    pythonCode += "cfg.put('wifi',{'ssid':'" + ssid + "','pwd':'" + pwd + "'})\n";
    return await this.write(pythonCode, function (value) {
      if (value.substring(0, 4) == 'save') {
        return { 'value': value, 'done': true };
      }
    });
  }

  async snapshot() {
    var val = await this.write(snapshotCode,
      async function (msg) {
        var value = msg;
        var done = false;
        if (value.substring(0, 8) == 'JPGSize:') {
          value = value.substring(8);
          done = true;
        }
        return { 'value': value, 'done': done }
      });
    this.stream.setReadByteArray(parseInt(val));
    var img = await this.write('repl.write(jpg)', async function (value) {
      var jpg = new Blob([value], { type: "image/jpeg" });
      var urlCreator = window.URL || window.webkitURL;
      return { 'value': urlCreator.createObjectURL(jpg), 'done': true };
    });
    this.stream.setReadLine();
    return img;
  }

}

```

main.js
```js=
define([
  'base/js/namespace',
  'jquery',
  'require',
  'base/js/events',
  'base/js/utils',
  './repl'
], function (Jupyter, $, requirejs, events, configmod, utils) {
  "use strict";
  var repl = new REPL();

  var usbBtn, runBtn;

  function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  function blink() {
    return setInterval(async function () {
      usbBtn.style.backgroundColor = '#ffffaa';
      await sleep(150);
      usbBtn.style.backgroundColor = '#aaaaaa';
      await sleep(150);
    }, 250)
  }

  var load_extension = function () {
    var btns = Jupyter.toolbar.add_buttons_group([
      Jupyter.keyboard_manager.actions.register({
          'help': 'connect to Web:Bit',
          'icon': 'fa-usb',
          'handler': async function () {
            await repl.usbConnect();
            repl.port.ondisconnect = function () {
              usbBtn.style.backgroundColor = '#ffaaaa';
              this.port = null;
            }            
            var clearId = blink();
            await repl.enter('esp32');
            await repl.write(`
import machine, neopixel
np = neopixel.NeoPixel(machine.Pin(4), 25)
for led in range(25):
  np[led] = (6,1,3)
  np.write()
np = neopixel.NeoPixel(machine.Pin(18), 25)
for led in range(25):
  np[led] = (6,1,3)
  np.write()
`);
            clearInterval(clearId);
            setTimeout(function () {
              usbBtn.style.backgroundColor = '#aaffaa';
            }, 300)
          }
        },
        'usb-connect',
        'usbconnect'),
      /*
      Jupyter.keyboard_manager.actions.register({
        'help': 'enter REPL',
        'icon': 'fa-cog',
        'handler': async function () {
            await repl.enterRAWREPL();
            setTimeout(async function(){
              await repl.sendCmd('from webai import *');
              await repl.sendCmd('webai.init()');
              await repl.sendCmd('webai.lcd.init()');
              usbBtn.style.backgroundColor='#aaffaa';
            },500);
        }
      }, 'usb-repl', 'usbrepl'),
      */
      Jupyter.keyboard_manager.actions.register({
        'help': 'Run code',
        'icon': 'fa-play',
        'handler': async function () {
          var nb = Jupyter.notebook;
          var idx = nb.get_anchor_index();
          var cell = nb.get_cell(idx);
          var code = cell.get_text();
          var output = '';
          cell.output_area.clear_output();
          await repl.write(code, function (value) {
            cell.output_area.append_output({
              "output_type": "display_data",
              "metadata": {}, // included to avoid warning
              "data": { "text/html": (value + "<br>") }
            });
            return { value: "", done: false }
          });
        }
      }, 'usb-run', 'usbrun'),
    ]);

    usbBtn = btns.find('button')[0];
    runBtn = btns.find('button')[1];
    usbBtn.style.backgroundColor = '#ffaaaa';
  };

  var extension = {
    load_jupyter_extension: load_extension,
    load_ipython_extension: load_extension
  };
  return extension;
})
```
