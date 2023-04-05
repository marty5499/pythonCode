###### tags: `chatgpt` `prompt` `webbit`

Web:Bit v2 自然語言編程 (2)
===

[MQTT測試網址](https://webbit.webduino.io/blockly/#XqDv82Zg8D0y5)
![](/uploads/upload_b4413cfa1e270a92e5788d79870b1aa4.png =45%x)

:::warning
你是專業的micropython老師
- 仔細讀開發版說明
- 按照開發版API用法 
- 根據問題撰寫完整程式
## 開發版說明
開發板類別 WebBit 有25顆燈,1排有5顆,由右至左總共5排,編號從0~24,
程式碼先import並初始化 wbit 實例
import time
from webduino.webbit import WebBit
wbit = WebBit()
## 開發板API
void show(int num,int r,int g,int b)
	num是第幾顆燈,rgb是顏色強度的數值 0~100
void showAll(int r,int g,int b)
	25顆燈全屏顯示,rgb是顏色強度的數值 0~100
int leftLight()
	左邊光度
int rightLight()
	右邊光度
int temp()
	溫度
void play(list)
	list可以放多個子list,一個子list有兩個元素,分別是播放頻率和播放時間(毫秒)
	例如播放 do,re list = [[262,0.25],[294,0.25]]
void pub(topicName,msg)
	透過mqtt傳送msg到指定的TopicName,msg需轉成字串格式
void sub(topicName,$callback)
	收到訊息呼叫指定方法
bool btnA()
	按下按鈕A
bool btnB()
	按下按鈕B
## 問題
- 彩燈用七彩流水燈方式呈現
- 每顆燈間隔速度0.006秒,點亮25顆燈
- 顯示藍色,黃色,綠色,紅色,粉紅色,紫色
- 重複上面步驟
:::


:::danger
你是專業的micropython老師
- 仔細讀開發版說明
- 按照開發版API用法
- 根據問題撰寫完整程式
## 開發版說明
有一開發板類別 WebBit,
開發板有25顆燈,1排有5顆,由右至左總共5排,編號從0~24,
程式碼先import並初始化 wbit 實例
from webduino.webbit import WebBit
wbit = WebBit()
## 開發板API
void show(int num,int r,int g,int b)
	num是第幾顆燈,rgb是顏色強度的數值 0~100
void showAll(int r,int g,int b)
	25顆燈全屏顯示,rgb是顏色強度的數值 0~100
int leftLight()
	左邊光度
int rightLight()
	右邊光度
int temp()
	溫度
void play(list)
	list可以放多個子list,一個子list有兩個元素,分別是播放頻率和播放時間(毫秒)
	例如播放 do,re list = [[262,0.25],[294,0.25]]
void pub(topicName,msg)
	透過mqtt傳送msg到指定的TopicName,msg需轉成字串格式
void sub(topicName,$callback)
	收到訊息呼叫指定方法
bool btnA()
	按下按鈕A
bool btnB()
	按下按鈕B
## 問題
:::


### 呼吸燈效果
:::info
使用呼吸燈效果，每隔1秒,全部顯示藍燈、綠燈、紅燈循環5次
:::

### 七彩彩燈
:::info
- 每隔0.01秒,依序使用白色,藍色,黃色,綠色,紅色,粉紅色,紫色點亮25顆燈
- 繼續重複上面步驟
:::

### 燈光秀
:::info
- 全部每顆燈都使用亂數的顏色
- 每隔0.001秒 , 重複上面步驟
:::

### 正方形
:::info
用紅色強度50,每隔0.25秒,點亮下面的燈號
0,1,2,3,4,9,14,19,24,23,22,21,20,15,10,5
:::

### 播放聲音
:::info
按下按鈕A播放 do re me
按下按鈕B播放 me re do
:::

### 光度太暗就發出聲音
:::info
- 每隔 0.1 秒偵測左右邊光度
- 當左邊光度值大於300時，顯示全屏綠色
- 當右邊邊光度值大於300時，顯示全屏紅色
- 當左右邊光度值都小於300時，發出beep三聲
:::

### 根據溫度點亮燈的數量
:::info
- 每隔0.1秒，讀取溫度數值
- 當溫度介於0~24之間時，就點亮webbit燈的數量，例如溫度24度，點亮24顆燈
- 燈的顏色用紅色，紅色的值為溫度數值 * 50
:::

### 偵測光度傳送到指定topic
:::info
- 每隔0.1秒，讀取左邊光度值
- 當光度值小於300，就將光度數值傳送到topic='qq'
- 當光度值小於300，25顆燈都顯示綠色
:::

### 小遊戲 (GPT-4可用)
:::info
第1顆燈顯示綠燈，經過0.25秒後，熄滅然後顯示第2顆燈，一直持續到第25顆燈，然後再循環從第1顆燈開始。
顯示燈號同時，偵測是否有按下按鈕A,如果按下按鈕A的時候，燈剛好顯示在第13顆燈，則發出 beep 3聲，並停止燈號顯示，否則就顯示紅色X，並結束程式

from webduino.webbit import WebBit
import time

def light_show(wbit):
    for i in range(25):
        wbit.show(i, 0, 255, 0)  # 綠光
        time.sleep(0.25)
        if wbit.btnA():
            if i == 12:  # 第13顆燈
                for _ in range(3):
                    wbit.play([262, 0.15])  # beep 3聲
                    time.sleep(0.2)
                break
            else:
                end_program(wbit)  # 顯示紅色X並結束程式
        wbit.show(i, 0, 0, 0)  # 熄滅

def end_program(wbit):
    for i in range(5):  # 顯示紅色X
        wbit.show(5 * i + i, 255, 0, 0)  # 上下對角線
        wbit.show(5 * i + 4 - i, 255, 0, 0)  # 下上對角線
    time.sleep(1)
    wbit.showAll(0, 0, 0)  # 熄滅
    exit(0)

wbit = WebBit()
while True:
    light_show(wbit)
:::