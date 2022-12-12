REPL 
===

## Interrupt ( Ctrl + C)
### *控制碼： \x03*

## Paste Mode 可以貼多行文字，每行有確認回傳字元 '='
### *進入控制碼：* \x05
### *完成控制碼：* \x04
### *取消控制碼：* \x03

## RAW Paste Mode 可以貼多行文字，不會有確認回傳字元
### *進入控制碼：* \x01
### *完成控制碼：* \x04 回傳 OK


```javascript=
// 產生 repl 物件
var repl = new REPL()

// 彈出對話框，連接 usb
await repl.usbConnect();

// 傳送指令等候確認
await repl.write("print(123)",function(resp){
    console.log("resp:",resp)
})


```