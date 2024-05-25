# uncompyle6 version 3.9.1
# Python bytecode version base 3.6 (3379)
# Decompiled from: Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)]
# Embedded file name: tcpClient.py
# Compiled at: 2024-02-24 18:06:18
# Size of source mod 2**32: 934 bytes
import socket

class init:

    def __init__(self, port=8003, timeOut=0):
        try:
            self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_client.settimeout(0.1)
            self.tcp_client.connect(("localhost", port))
            self.tcp_client.settimeout(timeOut)
            print("TCP连接成功,端口：" + str(port))
        except Exception as e:
            pass

    def request(self, date):
        try:
            self.tcp_client.send(date)
            recv = self.tcp_client.recv(1024)
        except Exception as e:
            recv = bytearray()

        return recv
