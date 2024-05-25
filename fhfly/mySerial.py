# uncompyle6 version 3.9.1
# Python bytecode version base 3.6 (3379)
# Decompiled from: Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)]
# Embedded file name: mySerial.py
# Compiled at: 2023-05-09 16:44:46
# Size of source mod 2**32: 1482 bytes
import serial, serial.tools.list_ports

class vcp:

    def __init__(self):
        self.device = False
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if "VID:PID=0483:5740" in p.hwid:
                self.device = p.device
                break

        if self.device:
            try:
                self.usart = serial.Serial((self.device), 460800, timeout=0.1)
            except Exception as e:
                print("串口打开异常，请检查是否已经关闭图形化编队软件！")
                self.device = False

        else:
            print("找不到设备,请检查遥控器是否成功连接到电脑！")

    def write(self, pack):
        try:
            self.usart.write(pack)
        except Exception as e:
            print("数据发送异常：", e)

    def read(self, size=1):
        try:
            return self.usart.read(size=size)
        except Exception as e:
            print("数据接收异常：", e)

    def any(self):
        try:
            return self.usart.inWaiting()
        except Exception as e:
            print("数据访问异常：", e)

    def writeStr(self, str):
        self.usart.write(str.encode("utf-8"))
