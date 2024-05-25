# uncompyle6 version 3.9.1
# Python bytecode version base 3.6 (3379)
# Decompiled from: Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)]
# Embedded file name: driver.py
# Compiled at: 2024-02-25 14:07:48
# Size of source mod 2**32: 4206 bytes
import sys, _thread
from .  import flyData
from time import sleep
MindPlus = 0
ESP32 = 1
掌控板 = 2
try:
    import uos
    from utime import ticks_ms
    if uos.uname().sysname == "esp32":
        driverType = ESP32
except Exception as e:
    from time import time
    driverType = MindPlus

class Rx(object):
    head = 0
    len = 0
    date = []
    cnt = 0
    state = 0
    buff = []
    fps = 0
    fpsCnt = 0


class init:

    def __init__(self, flyNum=1):
        self.rx = Rx()
        self.flyData = flyData.init(flyNum)
        if driverType == ESP32:
            from machine import UART, Pin
            self.uart = UART(2, 500000)
            self.uartEnable = True
            self.type = "ESP32"
        elif driverType == 掌控板:
            from machine import UART, Pin
            self.uart = UART(1, baudrate=500000, tx=(Pin.P16), rx=(Pin.P15))
            self.uartEnable = True
            self.type = "掌控板"
        else:
            from . import tcpClient
            from .mySerial import vcp
            self.tcp = tcpClient.init(port=8003)
            sleep(0.5)
            self.uart = vcp()
            if self.uart.device:
                self.uartEnable = True
            else:
                self.uartEnable = False
            self.type = "MindPlus"
        if self.uartEnable:
            _thread.start_new_thread(self.Receive_Thread, ())
            _thread.start_new_thread(self.Loop_1Hz_Thread, ())
            print("准备就绪，开始起飞。\n")
        else:
            sys.exit(1)

    def getSec(self):
        if driverType == MindPlus:
            return time()
        else:
            return ticks_ms() * 0.001

    def write(self, buff):
        self.uart.write(buff)

    def Receive_Prepare(self, data):
        if self.rx.state == 0:
            if data == 170:
                self.rx.state = 1
                self.rx.head = data
        elif self.rx.state == 1:
            if data > 0:
                if data < 30:
                    self.rx.state = 2
                    self.rx.len = data
                    self.rx.cnt = 0
            self.rx.state = 0
        elif self.rx.state == 2:
            pass
        self.rx.date.append(data)
        self.rx.cnt = self.rx.cnt + 1
        if self.rx.cnt >= self.rx.len:
            self.rx.state = 3
        elif self.rx.state == 3:
            self.rx.state = 0
            self.rx.date.append(data)
            self.Receive_Anl()
            self.rx.date = []
        else:
            self.rx.state = 0

    def Receive_Anl(self):
        sum = 0
        sum = self.rx.head + self.rx.len
        for temp in self.rx.date:
            sum = sum + temp

        sum = (sum - self.rx.date[self.rx.len]) % 256
        if sum != self.rx.date[self.rx.len]:
            return
        self.rx.fpsCnt = self.rx.fpsCnt + 1
        if self.rx.head == 170:
            self.flyData.Receive_Anl(self.rx)

    def Receive_Thread(self):
        while 1:
            packUart = self.uart.read(self.uart.any())
            size = len(packUart)
            for i in range(size):
                self.Receive_Prepare(packUart[i])

            if driverType == MindPlus:
                packVcp = self.tcp.request(packUart)
                if packVcp != None:
                    self.uart.write(packVcp)
                sleep(0.02)

    def Loop_1Hz_Thread(self):
        while True:
            self.rx.fps = self.rx.fpsCnt
            self.rx.fpsCnt = 0
            sleep(1)

    def run(self, time=-1):
        if time >= 0:
            sleep(time)
        else:
            print("程序运行完毕！")
