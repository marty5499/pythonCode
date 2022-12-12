###### tags: `micropython`
LoRa
====


https://escapequotes.net/esp32-lora-send-receive-packet-test/
![](/uploads/upload_a7639eee1370514135e94b7c3debcdea.png)
https://github.com/jpuk/simple-lora-esp32-test/tree/master/heltec


### [規格書](http://m.asnwireless.com/uploads/201922129/Specification-of-AS32-TTL-100.pdf) [網路範例](https://www.cnblogs.com/allofalan/p/12238149.html)

- [LoRa模块介绍及选型攻略](https://blog.csdn.net/AshiningFAE/article/details/120348165?spm=1001.2101.3001.6650.17&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-17.pc_relevant_default&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7Edefault-17.pc_relevant_default&utm_relevant_index=21)
- [模式說明](https://www.bilibili.com/read/cv7593287)

![](/uploads/upload_e5af7c8cd17b6920d6304d262417dde4.png)

```c=
#include <SoftwareSerial.h>
const int LedPin = 2;
SoftwareSerial s1(3, 4); // RX, TX
int isHigh = 0 ;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  
  s1.begin(9600);
  pinMode(LedPin, OUTPUT);
}

void loop() {
  if (s1.available())
  {
    delay(50);
    int val = s1.read();
    Serial.println(val);
    for (int i = 0; i < 10; i++) {
      flashLed();
    }
  }
}

void flashLed() {  
  digitalWrite(LedPin, HIGH);
  delay(100);
  digitalWrite(LedPin, LOW);
  delay(100); 
}
```