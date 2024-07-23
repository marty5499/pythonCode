import bluetooth, random, struct, time, _thread
from ubluetooth import BLE
from micropython import const

_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATTS_WRITE = const(3)
_IRQ_GATTS_READ_REQUEST = const(4)
_IRQ_SCAN_RESULT = const(5)
_IRQ_SCAN_DONE = const(6)
_IRQ_PERIPHERAL_CONNECT = const(7)
_IRQ_PERIPHERAL_DISCONNECT = const(8)
_IRQ_GATTC_SERVICE_RESULT = const(9)
_IRQ_GATTC_SERVICE_DONE = const(10)
_IRQ_GATTC_CHARACTERISTIC_RESULT = const(11)
_IRQ_GATTC_CHARACTERISTIC_DONE = const(12)
_IRQ_GATTC_DESCRIPTOR_RESULT = const(13)
_IRQ_GATTC_DESCRIPTOR_DONE = const(14)
_IRQ_GATTC_READ_RESULT = const(15)
_IRQ_GATTC_READ_DONE = const(16)
_IRQ_GATTC_WRITE_DONE = const(17)
_IRQ_GATTC_NOTIFY = const(18)
_IRQ_GATTC_INDICATE = const(19)
_IRQ_GATTS_INDICATE_DONE = const(20)
_IRQ_MTU_EXCHANGED = const(21)
_IRQ_L2CAP_ACCEPT = const(22)
_IRQ_L2CAP_CONNECT = const(23)
_IRQ_L2CAP_DISCONNECT = const(24)
_IRQ_L2CAP_RECV = const(25)
_IRQ_L2CAP_SEND_READY = const(26)
_IRQ_CONNECTION_UPDATE = const(27)
_IRQ_ENCRYPTION_UPDATE = const(28)
_IRQ_GET_SECRET = const(29)
_IRQ_SET_SECRET = const(30)

_FLAG_BROADCAST = const(0x0001)
_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)
_FLAG_INDICATE = const(0x0020)
_FLAG_AUTHENTICATED_SIGNED_WRITE = const(0x0040)
_FLAG_AUX_WRITE = const(0x0100)
_FLAG_READ_ENCRYPTED = const(0x0200)
_FLAG_READ_AUTHENTICATED = const(0x0400)
_FLAG_READ_AUTHORIZED = const(0x0800)
_FLAG_WRITE_ENCRYPTED = const(0x1000)
_FLAG_WRITE_AUTHENTICATED = const(0x2000)
_FLAG_WRITE_AUTHORIZED = const(0x4000)

mi_addr = b''
conn_handle = 0

_UART_UUID = bluetooth.UUID("ebe0ccb0-7a0a-4b0c-8a1a-6ff2997da3a6")
_UART_TX = (
    bluetooth.UUID("ebe0ccc1-7a0a-4b0c-8a1a-6ff2997da3a6"),
    _FLAG_READ | _FLAG_NOTIFY,
)

_UART_SERVICE = (
    _UART_UUID,
    (_UART_TX,),
)

def transdata(pData):
    temp = (pData[0] | (pData[1] << 8)) * 0.01
    humi = pData[2]
    voltage = (pData[3] | (pData[4] << 8)) * 0.001
    return temp, humi, voltage

def btirq(event, data):
    global mi_addr, conn_handle
    if event == _IRQ_CENTRAL_CONNECT:
        conn_handle, _, _ = data
        print("New connection", conn_handle)
    elif event == _IRQ_PERIPHERAL_CONNECT:
        conn_handle, addr_type, addr = data
        print(conn_handle)
        print('connected!')
        # bt.gattc_discover_services(0, _UART_UUID)
        # bt.gattc_discover_characteristics(0, 33, 78)  # value_handle 64
    elif event == _IRQ_GATTS_WRITE:
        conn_handle, value_handle, data = data
    elif event == _IRQ_GATTC_SERVICE_RESULT:
        conn_handle, start_handle, end_handle, uuid = data
        print(conn_handle, start_handle, end_handle, uuid)
    elif event == _IRQ_GATTC_READ_RESULT:
        print('mi data')
        conn_handle, value_handle, char_data = data
        bytedata = bytes(char_data)
        print(transdata(bytedata))
    elif event == _IRQ_PERIPHERAL_DISCONNECT:
        print('disconnected')
    elif event == _IRQ_SCAN_RESULT:
        addr_type, addr, adv_type, rssi, adv_data = data
        if bytes(adv_data)[0:6] == b'\x02\x01\x06\x11\x16\x95':
            print('found you!!!')
            mi_addr = bytes(addr)
    elif event == _IRQ_SCAN_DONE:
        print('scan finished!')
        print(mi_addr)
    elif event == _IRQ_GATTC_SERVICE_DONE:
        print("_IRQ_GATTC_SERVICE_DONE")
    elif event == _IRQ_GATTC_CHARACTERISTIC_RESULT:
        conn_handle, end_handle, value_handle, properties, uuid = data
        print(value_handle, uuid, properties)
    elif event == _IRQ_GATTC_CHARACTERISTIC_DONE:
        conn_handle, status = data
    elif event == _IRQ_GATTC_NOTIFY:
        conn_handle, value_handle, notify_data = data
        # A server has sent a notify request.
    elif event == _IRQ_GATTC_INDICATE:
        conn_handle, value_handle, notify_data = data
        # A server has sent an indicate request.
    elif event == _IRQ_GATTS_INDICATE_DONE:
        conn_handle, value_handle, status = data

bt = BLE()
bt.active(True)
bt.irq(btirq)
print('BLE ON! SEARCHING FOR MI DEVICES...')
bt.gap_scan(5000, 10000, 10000)
time.sleep(6)
# mi_addr = b'\xa4\xc1$\x10\x9d'
bt.gap_connect(0, mi_addr, 10000)
time.sleep(5)
# bt.gattc_discover_services(0)
while 1:
    bt.gattc_read(conn_handle, 54)
    # bt.gatts_notify(conn_handle, 64)
    print('try to read')
    time.sleep(1)


