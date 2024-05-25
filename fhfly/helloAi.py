# uncompyle6 version 3.9.1
# Python bytecode version base 3.6 (3379)
# Decompiled from: Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)]
# Embedded file name: helloAi.py
# Compiled at: 2024-02-29 12:29:30
# Size of source mod 2**32: 2313 bytes
import _thread
from . import tcpClient
from time import sleep

class init:

    def __init__(self):
        self.cmdString = ""
        self.reqDict = {}
        self.ai = tcpClient.init(port=8004, timeOut=0.01)
        _thread.start_new_thread(self.run, ())

    def run(self):
        while True:
            string = self.cmdString
            self.cmdString = "GET /poll HTTP/1.1"
            self.request(string)
            sleep(0.02)

    def request(self, cmdString):
        lines = self.ai.request(cmdString.encode("utf-8")).decode("utf-8").splitlines()
        lens = len(lines)
        for i in range(lens):
            words = lines[i].split()
            if len(words) == 1:
                self.reqDict[words[0]] = ""
            else:
                if len(words) > 1:
                    self.reqDict[words[0]] = words[1]

    def getKeyValue(self, key):
        try:
            value = self.reqDict[key]
        except:
            value = ""

        return value

    def runFunction(self, function):
        self.cmdString = "GET /aiCtrl/" + function
        self.reqDict["aiFinish"] = "false"
        sleep(0.1)

    def isComplete(self):
        if self.getKeyValue("aiFinish") == "true":
            return True
        else:
            return False

    def result(self, details):
        result = self.getKeyValue("aiResult/" + details)
        if details != "文字内容":
            result = self.strToInt(result)
        return result

    def resultFace(self, num, details):
        result = self.getKeyValue("aiResultFace/" + str(num) + "/" + details)
        if details != "名字":
            result = self.strToInt(result)
        return result

    def resultObject(self, num, details):
        result = self.getKeyValue("aiResultObject/" + str(num) + "/" + details)
        if details != "名称":
            result = self.strToInt(result)
        return result

    def strToInt(self, string):
        try:
            result = int(float(string))
        except:
            result = 0

        return result


if __name__ == "__main__":
    test = init()
    test.runFunction("文字识别")
