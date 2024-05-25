# uncompyle6 version 3.9.1
# Python bytecode version base 3.6 (3379)
# Decompiled from: Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)]
# Embedded file name: helloFly.py
# Compiled at: 2024-03-31 11:59:30
# Size of source mod 2**32: 27867 bytes
import os, math
from . import driver
from math import sqrt
from struct import pack
from random import randint

class order(object):
    takeOff = 0
    flyMode = 1
    xySpeed = 2
    zSpeed = 3
    followLine = 4
    moveCtrl = 5
    moveSearchDot = 6
    moveSearchTag = 7
    moveSearchBlob = 8
    goTo = 9
    rotation = 10
    flyHigh = 11
    flipCtrl = 12
    ledCtrl = 13
    mvMode = 14
    magnetCtrl = 15
    servoCtrl = 16
    roleCtrl = 17
    lockDir = 18
    shootCtrl = 19
    switchCtrl = 20
    moveFollowTag = 21
    photographMode = 22
    goToTag = 23
    move = 24
    serServoCtrl = 25
    robotArmCtrl = 26
    robotArmRecord = 27
    robotArmFree = 28
    robotArmCover = 29
    setLocation = 30
    setTagDistance = 31
    setCenterOffset = 32
    cameraDeg = 33
    showStr = 34
    showCtrl = 35
    irSend = 36
    tofSwitch = 37
    fmaInit = 253
    flyCtrl = 254
    nullCmd = 255


class fly:

    def __init__(self):
        self.maxNum = 10
        self.setTime = 0.5
        self.isDelay = True
        self.horSpeed = 100
        self.verSpeed = 100
        self.count = randint(0, 255)
        self.port = driver.init(self.maxNum)
        self.timerStart = self.getTicks_sec()
        self.timeSec = [self.getTicks_sec() for _ in range(self.maxNum)]
        try:
            from .myVoice import textToSpeed
            self.voice = textToSpeed()
        except Exception as e:
            self.voice = False

    def getTicks_sec(self):
        return self.port.getSec()

    def getTimer(self):
        return self.getTicks_sec() - self.timerStart

    def clearTimer(self):
        self.timerStart = self.getTicks_sec()

    def showText(self, id, string):
        nowTime = self.getTicks_sec()
        dT = nowTime - self.timeSec[id]
        self.timeSec[id] = nowTime
        if self.port.type == "OpenMV":
            if dT >= 0.1:
                print("---" + "%.1f" % dT + "s")
            print(string)
        else:
            if dT >= 0.1:
                print("\x1b[1;34m---" + "%.1f" % dT + "s" + "\x1b[0m")
            print("\x1b[1;30m" + string + "\x1b[0m")

    def pyLink_pack(self, fun, buff):
        sum = 0
        pack_data = bytearray([187, 0, fun])
        pack_data.extend(buff)
        pack_data[1] = len(pack_data) - 2
        for temp in pack_data:
            sum = sum + temp

        pack_data.extend(pack("<B", sum % 256))
        return pack_data

    def sendOrderPack(self, id, cmd, pack):
        self.count = self.count + 1
        buff = bytearray([id, cmd, self.count % 256])
        buff = buff + pack
        dLen = 13 - len(buff)
        if dLen > 0:
            buff.extend(bytearray(dLen))
        self.port.write(self.pyLink_pack(243, buff + buff + bytearray([100, 0])))

    def sendOrder(self, id, cmd, fmt, *args):
        self.sendOrderPack(id, cmd, pack(fmt, *args))

    def sleep(self, sec):
        self.port.run(sec)

    def setAutoDelay(self, auto):
        self.isDelay = auto

    def tts(self, string, wait=True):
        if self.voice:
            self.voice.speak(string, wait)
        else:
            print("语音播报：" + string)

    def moveDelay(self, id):
        if self.isDelay:
            self.sleep(1)
            dis = 100
            while dis > 10:
                self.sleep(0.1)
                dx = self.port.flyData.flySensor[id].locErr[0]
                dy = self.port.flyData.flySensor[id].locErr[1]
                dz = self.port.flyData.flySensor[id].locErr[2]
                dis = sqrt(dx * dx + dy * dy + dz * dz)

            self.sleep(1)
        else:
            self.sleep(0.1)

    def autoDelay(self, sec):
        if self.isDelay:
            self.sleep(sec)
        else:
            self.sleep(0.1)

    def takeOff(self, id, high):
        high = int(high + 0.5)
        self.sendOrder(id, order.takeOff, "<h2B2h", high, 50, 0, 0, 0)
        self.showText(id, "takeOff(" + str(id) + "," + str(high) + ")")
        self.autoDelay(3 + high / 100)

    def flyCtrl(self, id, mode):
        self.sendOrder(id, order.flyCtrl, "<B", mode)
        self.showText(id, "flyCtrl(" + str(id) + "," + str(mode) + ")")
        self.autoDelay(3)

    def flyMode(self, id, mode):
        self.sendOrder(id, order.flyMode, "<B", mode)
        self.showText(id, "flyMode(" + str(id) + "," + str(mode) + ")")
        self.autoDelay(self.setTime)

    def xySpeed(self, id, speed):
        speed = int(speed + 0.5)
        self.horSpeed = speed
        self.sendOrder(id, order.xySpeed, "<h", speed)
        self.showText(id, "xySpeed(" + str(id) + "," + str(speed) + ")")
        self.autoDelay(self.setTime)

    def zSpeed(self, id, speed):
        speed = int(speed + 0.5)
        self.verSpeed = speed
        self.sendOrder(id, order.zSpeed, "<h", speed)
        self.showText(id, "zSpeed(" + str(id) + "," + str(speed) + ")")
        self.autoDelay(self.setTime)

    def move(self, id, mode, loc):
        loc[0] = int(loc[0] + 0.5)
        loc[1] = int(loc[1] + 0.5)
        loc[2] = int(loc[2] + 0.5)
        self.sendOrder(id, order.move, "<B3h", mode, int(loc[0]), int(loc[1]), int(loc[2]))
        self.showText(id, "move(" + str(id) + "," + str(mode) + ",[" + str(loc[0]) + "," + str(loc[1]) + "," + str(loc[2]) + "])")
        self.moveDelay(id)

    def moveCtrl(self, id, dir, distance):
        if dir > 6:
            distance = int(distance * 0.7071 + 0.5)
        else:
            distance = int(distance + 0.5)
        self.sendOrder(id, order.moveCtrl, "<Bh", dir, distance)
        self.showText(id, "moveCtrl(" + str(id) + "," + str(dir) + "," + str(distance) + ")")
        self.moveDelay(id)

    def moveSearchDot(self, id, dir, distance):
        if dir > 6:
            distance = int(distance * 0.7071 + 0.5)
        else:
            distance = int(distance + 0.5)
        self.sendOrder(id, order.moveSearchDot, "<Bh", dir, distance)
        self.showText(id, "moveSearchDot(" + str(id) + "," + str(dir) + "," + str(distance) + ")")
        self.moveDelay(id)

    def moveSearchBlob(self, id, dir, distance, blob):
        if dir > 6:
            distance = int(distance * 0.7071 + 0.5)
        else:
            distance = int(distance + 0.5)
        self.sendOrder(id, order.moveSearchBlob, "<Bh6b", dir, distance, blob[0], blob[1], blob[2], blob[3], blob[4], blob[5])
        self.showText(id, "moveSearchDot(" + str(id) + "," + str(dir) + "," + str(distance) + ",[" + str(blob[0]) + "," + str(blob[1]) + "," + str(blob[2]) + "," + str(blob[3]) + "," + str(blob[4]) + "," + str(blob[5]) + "])")
        self.moveDelay(id)

    def moveSearchTag(self, id, dir, distance, tagID):
        if dir > 6:
            distance = int(distance * 0.7071 + 0.5)
        else:
            distance = int(distance + 0.5)
        self.sendOrder(id, order.moveSearchTag, "<Bhh", dir, distance, tagID)
        self.showText(id, "moveSearchTag(" + str(id) + "," + str(dir) + "," + str(distance) + "," + str(tagID) + ")")
        self.moveDelay(id)

    def moveFollowTag(self, id, dir, distance, tagID):
        if dir > 6:
            distance = int(distance * 0.7071 + 0.5)
        else:
            distance = int(distance + 0.5)
        self.sendOrder(id, order.moveFollowTag, "<Bhh", dir, distance, tagID)
        self.showText(id, "moveFollowTag(" + str(id) + "," + str(dir) + "," + str(distance) + "," + str(tagID) + ")")
        self.moveDelay(id)

    def goTo(self, id, loc):
        loc[0] = int(loc[0] + 0.5)
        loc[1] = int(loc[1] + 0.5)
        loc[2] = int(loc[2] + 0.5)
        self.sendOrder(id, order.goTo, "<3h", loc[0], loc[1], loc[2])
        self.showText(id, "goTo(" + str(id) + ",[" + str(loc[0]) + "," + str(loc[1]) + "," + str(loc[2]) + "])")
        self.moveDelay(id)

    def goToTag(self, id, tagID, high):
        high = int(high + 0.5)
        self.sendOrder(id, order.goToTag, "<2h", tagID, high)
        self.showText(id, "goToTag(" + str(id) + "," + str(tagID) + "," + str(high) + ")")
        self.moveDelay(id)

    def rotation(self, id, angle):
        angle = int(angle + 0.5)
        self.sendOrder(id, order.rotation, "<h", angle)
        self.showText(id, "rotation(" + str(id) + "," + str(angle) + ")")
        self.autoDelay(1 + abs(angle) / 20)

    def flyHigh(self, id, high):
        high = int(high + 0.5)
        self.sendOrder(id, order.flyHigh, "<h", high)
        self.showText(id, "flyHigh(" + str(id) + "," + str(high) + ")")
        self.moveDelay(id)

    def tofSwitch(self, id, mode):
        self.sendOrder(id, order.tofSwitch, "<B", mode)
        self.showText(id, "tofSwitch(" + str(id) + "," + str(mode) + ")")
        self.autoDelay(self.setTime)

    def flipCtrl(self, id, dir, cir):
        self.sendOrder(id, order.flipCtrl, "<2B", dir, cir)
        self.showText(id, "flipCtrl(" + str(id) + "," + str(dir) + "," + str(cir) + ")")
        self.autoDelay(2)

    def ledCtrl(self, id, mode, color):
        color[0] = int(color[0] + 0.5)
        color[1] = int(color[1] + 0.5)
        color[2] = int(color[2] + 0.5)
        self.sendOrder(id, order.ledCtrl, "<4B", mode, color[0], color[1], color[2])
        self.showText(id, "ledCtrl(" + str(id) + "," + str(mode) + ",[" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + "])")
        self.autoDelay(self.setTime)

    def closeLed(self, id):
        self.sendOrder(id, order.ledCtrl, "<4B", 0, 0, 0, 0)
        self.showText(id, str(id) + "号关闭灯光")
        self.autoDelay(self.setTime)

    def mvCheckMode(self, id, mode):
        self.sendOrder(id, order.mvMode, "<B6bh", mode, 0, 0, 0, 0, 0, 0, 0)
        self.showText(id, "mvCheckMode(" + str(id) + "," + str(mode) + ")")
        self.autoDelay(self.setTime)

    def mvCheckTag(self, id, tagID):
        self.sendOrder(id, order.mvMode, "<B6bh", 6, 0, 0, 0, 0, 0, 0, tagID)
        self.showText(id, "mvCheckTag(" + str(id) + "," + str(tagID) + ")")
        self.autoDelay(self.setTime)

    def mvCheckBlob(self, id, type, blob):
        self.sendOrder(id, order.mvMode, "<B6bh", type, blob[0], blob[1], blob[2], blob[3], blob[4], blob[5], 0)
        self.showText(id, "mvCheckBlob(" + str(id) + ",[" + str(blob[0]) + "," + str(blob[1]) + "," + str(blob[2]) + "," + str(blob[3]) + "," + str(blob[4]) + "," + str(blob[5]) + "])")
        self.autoDelay(self.setTime)

    def shootCtrl(self, id, mode):
        self.sendOrder(id, order.shootCtrl, "<B", mode)
        self.showText(id, "shootCtrl(" + str(id) + "," + str(mode) + ")")
        self.autoDelay(self.setTime)

    def magnetCtrl(self, id, mode):
        self.sendOrder(id, order.magnetCtrl, "<B", mode)
        self.showText(id, "magnetCtrl(" + str(id) + "," + str(mode) + ")")
        self.autoDelay(self.setTime)

    def servoCtrl(self, id, angle):
        angle = int(angle + 0.5)
        self.sendOrder(id, order.servoCtrl, "<B", angle)
        self.showText(id, "servoCtrl(" + str(id) + "," + str(angle) + ")")
        self.autoDelay(self.setTime)

    def lockDir(self, id, mode):
        self.sendOrder(id, order.lockDir, "<B", mode)
        self.showText(id, "lockDir(" + str(id) + "," + str(mode) + ")")
        self.autoDelay(self.setTime)

    def roleCtrl(self, id, string):
        strBuf = string.encode("utf-8")
        strLen = len(strBuf)
        if strLen < 11:
            self.sendOrderPack(id, order.roleCtrl, strBuf)
            self.showText(id, "roleCtrl(" + str(id) + ',"' + string + '")')
            self.autoDelay(self.setTime)
        else:
            self.showText(id, "发送失败：字符超过10字节")

    def setCenterOffset(self, id, offset):
        self.sendOrder(id, order.setCenterOffset, "<2h", offset[0], offset[1])
        self.showText(id, "setCenterOffset(" + str(id) + ",[" + str(offset[0]) + "," + str(offset[1]) + "])")
        self.autoDelay(self.setTime)

    def setLocation(self, id, loc):
        self.sendOrder(id, order.setLocation, "<2h", loc[0], loc[1])
        self.showText(id, "setLocation(" + str(id) + ",[" + str(loc[0]) + "," + str(loc[1]) + "])")
        self.autoDelay(self.setTime)

    def setTagDistance(self, id, distance):
        self.sendOrder(id, order.setTagDistance, "<h", distance)
        self.showText(id, "setTagDistance(" + str(id) + "," + str(distance) + ")")
        self.autoDelay(self.setTime)

    def cameraDeg(self, id, deg):
        self.sendOrder(id, order.cameraDeg, "<h", deg)
        self.showText(id, "cameraDeg(" + str(id) + "," + str(deg) + ")")
        self.autoDelay(self.setTime)

    def photographMode(self, id, mode):
        self.port.flyData.photo.id = id
        self.port.flyData.photo.isOk = False
        self.sendOrder(id, order.photographMode, "<B", mode)
        self.showText(id, "photographMode(" + str(id) + "," + str(mode) + ")")
        self.autoDelay(self.setTime)

    def irSend(self, id, mode, data):
        self.sendOrder(id, order.irSend, "<5B", mode, data[0], data[1], data[2], data[3])
        self.showText(id, "irSend(" + str(id) + "," + str(mode) + ",[" + hex(data[0]) + "," + hex(data[1]) + "," + hex(data[2]) + "," + hex(data[3]) + "])")
        self.autoDelay(self.setTime)

    def showStr(self, id, x, y, string, scal):
        buf = pack("<3B", x, y, scal)
        strBuf = string.encode("utf-8")
        strLen = len(strBuf)
        if strLen <= 7:
            self.sendOrderPack(id, order.showStr, buf + strBuf)
            self.showText(id, "showStr(" + str(id) + "," + str(x) + "," + str(y) + ',"' + string + '",' + str(scal) + ")")
            self.autoDelay(self.setTime)
        else:
            self.showText(id, "显示失败：字符超过7字节")

    def showCtrl(self, id, mode):
        self.sendOrder(id, order.showCtrl, "<B", mode)
        self.showText(id, "showCtrl(" + str(id) + "," + str(mode) + ")")
        self.autoDelay(self.setTime)

    def photoOk(self):
        return self.port.flyData.photo.isOk

    def isPhotoOk(self):
        return self.photoOk()

    def getKeyPress(self, id):
        if self.port.flyData.keyPressId == id:
            return True
        else:
            return False

    def isMvCheck(self, id, mode):
        return self.port.flyData.flySensor[id].mv.flag & 1 << mode != 0

    def isMvCheckLine(self, id, dir):
        return self.port.flyData.flySensor[id].mv.flag & 1 << dir != 0

    def getObsDistance(self, id, dir):
        return round(self.port.flyData.flySensor[id].obs_dist[dir], 1)

    def getFlySensor(self, id, type):
        if type == "tagID":
            return self.port.flyData.flySensor[id].mv.tagId
        else:
            if type == "qrCode":
                return self.port.flyData.flySensor[id].qrCode
            else:
                if type == "brCode":
                    return self.port.flyData.flySensor[id].brCode
                else:
                    if type == "rol":
                        return round(self.port.flyData.flySensor[id].imu[0], 1)
                    else:
                        if type == "pit":
                            return round(self.port.flyData.flySensor[id].imu[1], 1)
                        else:
                            if type == "yaw":
                                return round(self.port.flyData.flySensor[id].imu[2], 1)
                            else:
                                if type == "loc_x":
                                    return round(self.port.flyData.flySensor[id].loc[0], 1)
                                if type == "loc_y":
                                    return round(self.port.flyData.flySensor[id].loc[1], 1)
                            if type == "loc_z":
                                return round(self.port.flyData.flySensor[id].loc[2], 1)
                        if type == "err_x":
                            return round(self.port.flyData.flySensor[id].locErr[0], 1)
                    if type == "err_y":
                        return round(self.port.flyData.flySensor[id].locErr[1], 1)
                if type == "err_z":
                    return round(self.port.flyData.flySensor[id].locErr[2], 1)
            if type == "vol":
                return round(self.port.flyData.flySensor[id].vol, 2)

    def getBlobResult(self, id, type):
        if type == "s":
            return self.port.flyData.flySensor[id].mv.blob_s
        else:
            if type == "w":
                return self.port.flyData.flySensor[id].mv.blob_w
            if type == "h":
                return self.port.flyData.flySensor[id].mv.blob_h
            if type == "n":
                return self.port.flyData.flySensor[id].mv.blob_n

    def getRoleNews(self, id, type):
        if type == "details":
            return self.port.flyData.flySensor[id].news
        if type == "id":
            return self.port.flyData.flySensor[id].newsCount

    def clearRoleNews(self, id):
        self.port.flyData.flySensor[id].news = ""

    def clearConsole(self):
        try:
            os.system("cls")
            self.sleep(0.1)
        except:
            pass

    def switchCtrl(self, id, mode):
        self.sendOrder(id, order.switchCtrl, "<B", mode)
        self.showText(id, "switchCtrl(" + str(id) + "," + str(mode) + ")")
        self.autoDelay(self.setTime)

    def getScaleWeight(self, id):
        return self.port.flyData.flySensor[id].scale_weight

    def getShootResult(self, id, type):
        if type == "number":
            return self.port.flyData.flySensor[id].laserTarget_count
        else:
            if type == "result":
                return self.port.flyData.flySensor[id].laserTarget_result
            if type == "x":
                return self.port.flyData.flySensor[id].laserTarget_x
            if type == "y":
                return self.port.flyData.flySensor[id].laserTarget_y

    def serServoCtrl(self, id, index, value, time):
        self.sendOrder(id, order.serServoCtrl, "<B2h", index, value, time)
        self.showText(id, "serServoCtrl(" + str(id) + "," + str(index) + "," + str(value) + "," + str(time) + ")")
        self.autoDelay(time * 0.001)

    def robotArmCtrl(self, id, index, time):
        self.sendOrder(id, order.robotArmCtrl, "<Bh", index, time)
        self.showText(id, "robotArmCtrl(" + str(id) + "," + str(index) + "," + str(time) + ")")
        self.autoDelay(time * 0.001)

    def robotArmCover(self, id, index):
        self.sendOrder(id, order.robotArmCover, "<B", index)
        self.showText(id, "robotArmCover(" + str(id) + "," + str(index) + ")")
        self.autoDelay(self.setTime)

    def robotArmRecord(self, id, mode):
        self.sendOrder(id, order.robotArmRecord, "<B", mode)
        self.showText(id, "robotArmRecord(" + str(id) + "," + str(mode) + ")")
        self.autoDelay(self.setTime)

    def ShuiPingHuanRao(self, id, type, X, Y, A, S):
        self.showText(id, str(id) + "号机，开始水平环绕...")
        self.sleep(1)
        self.setAutoDelay(0)
        self.zSpeed(id, 100)
        self.xySpeed(id, 100)
        if type:
            X = self.getFlySensor(id, "loc_x") + self.getFlySensor(id, "err_x") + X
            Y = self.getFlySensor(id, "loc_y") + self.getFlySensor(id, "err_y") + Y
        dx = self.getFlySensor(id, "loc_x") + self.getFlySensor(id, "err_x") - X
        dy = self.getFlySensor(id, "loc_y") + self.getFlySensor(id, "err_y") - Y
        dz = self.getFlySensor(id, "loc_z") + self.getFlySensor(id, "err_z") - 0
        HuanRaoBanJing = math.sqrt(dx * dx + dy * dy)
        HuanRaoBuJu = 0.1 * S / (6.28 * HuanRaoBanJing) * 360
        HuanRaoChuShiJiaoDu = math.atan2(dx, dy) * 57.29
        YiHuanRaoDeJiaoDu = 0
        while not abs(YiHuanRaoDeJiaoDu) >= abs(A):
            if A < 0:
                YiHuanRaoDeJiaoDu = YiHuanRaoDeJiaoDu - HuanRaoBuJu
            else:
                YiHuanRaoDeJiaoDu = YiHuanRaoDeJiaoDu + HuanRaoBuJu
            HuanRaoShiShiJiaoDu = HuanRaoChuShiJiaoDu + YiHuanRaoDeJiaoDu
            ShiShix = X + HuanRaoBanJing * math.sin(math.radians(HuanRaoShiShiJiaoDu))
            ShiShiy = Y + HuanRaoBanJing * math.cos(math.radians(HuanRaoShiShiJiaoDu))
            ShiShiz = dz
            self.goTo(id, [ShiShix, ShiShiy, ShiShiz])

        self.sleep(1)
        self.setAutoDelay(1)
        self.zSpeed(id, S)
        self.xySpeed(id, S)

    def ChuiZhiHuanRao(self, id, dir, D, Z, A, S):
        self.showText(id, str(id) + "号机，开始垂直环绕...")
        self.sleep(1)
        self.setAutoDelay(0)
        self.zSpeed(id, 100)
        self.xySpeed(id, 100)
        dz = self.getFlySensor(id, "loc_z") + self.getFlySensor(id, "err_z") - Z
        if dir.find("LR") != -1:
            D = self.getFlySensor(id, "loc_x") + self.getFlySensor(id, "err_x") + D
            dx = self.getFlySensor(id, "loc_x") + self.getFlySensor(id, "err_x") - D
            dy = self.getFlySensor(id, "loc_y") + self.getFlySensor(id, "err_y") - 0
            HuanRaoBanJing = math.sqrt(dx * dx + dz * dz)
            HuanRaoChuShiJiaoDu = math.atan2(dx, dz) * 57.29
        else:
            D = self.getFlySensor(id, "loc_y") + self.getFlySensor(id, "err_y") + D
            dx = self.getFlySensor(id, "loc_x") + self.getFlySensor(id, "err_x") - 0
            dy = self.getFlySensor(id, "loc_y") + self.getFlySensor(id, "err_y") - D
            HuanRaoBanJing = math.sqrt(dy * dy + dz * dz)
            HuanRaoChuShiJiaoDu = math.atan2(dy, dz) * 57.29
        HuanRaoBuJu = 0.1 * S / (6.28 * HuanRaoBanJing) * 360
        YiHuanRaoDeJiaoDu = 0
        while not abs(YiHuanRaoDeJiaoDu) >= abs(A):
            if A < 0:
                YiHuanRaoDeJiaoDu = YiHuanRaoDeJiaoDu - HuanRaoBuJu
            else:
                YiHuanRaoDeJiaoDu = YiHuanRaoDeJiaoDu + HuanRaoBuJu
            HuanRaoShiShiJiaoDu = HuanRaoChuShiJiaoDu + YiHuanRaoDeJiaoDu
            if dir.find("LR") != -1:
                ShiShix = D + HuanRaoBanJing * math.sin(math.radians(HuanRaoShiShiJiaoDu))
                ShiShiy = dy
            else:
                ShiShix = dx
                ShiShiy = D + HuanRaoBanJing * math.sin(math.radians(HuanRaoShiShiJiaoDu))
            ShiShiz = Z + HuanRaoBanJing * math.cos(math.radians(HuanRaoShiShiJiaoDu))
            self.goTo(id, [ShiShix, ShiShiy, ShiShiz])

        self.sleep(1)
        self.setAutoDelay(1)
        self.zSpeed(id, S)
        self.xySpeed(id, S)

    def ZhengXianHuanRao(self, id, dir, A0, A1, L, H, S):
        self.showText(id, str(id) + "号机，开始正弦环绕...")
        self.sleep(1)
        self.setAutoDelay(0)
        self.zSpeed(id, 100)
        self.xySpeed(id, 100)
        ChuShix = self.getFlySensor(id, "loc_x") + self.getFlySensor(id, "err_x")
        ChuShiy = self.getFlySensor(id, "loc_y") + self.getFlySensor(id, "err_y")
        ChuShiz = self.getFlySensor(id, "loc_z") + self.getFlySensor(id, "err_z")
        HuanRaoBuJu = 0.1 * S / math.sqrt(L * L + 4 * H * 4 * H) * 360
        YiHuanRaoDeJiaoDu = 0
        while not abs(YiHuanRaoDeJiaoDu) >= abs(A0 - A1):
            if A1 < A0:
                YiHuanRaoDeJiaoDu = YiHuanRaoDeJiaoDu - HuanRaoBuJu
            else:
                YiHuanRaoDeJiaoDu = YiHuanRaoDeJiaoDu + HuanRaoBuJu
            HuanRaoShiShiJiaoDu = A0 + YiHuanRaoDeJiaoDu
            ShiShix = ChuShix + (HuanRaoShiShiJiaoDu - A0) / 360 * L
            ShiShiy = ChuShiy + math.sin(math.radians(A0 + HuanRaoShiShiJiaoDu)) * H
            ShiShiz = ChuShiz
            if dir.find("FB") != -1:
                if dir.find("VER") != -1:
                    ShiShix = ChuShix
                    ShiShiy = ChuShiy + (HuanRaoShiShiJiaoDu - A0) / 360 * L
                    ShiShiz = ChuShiz + math.sin(math.radians(A0 + HuanRaoShiShiJiaoDu)) * H
                else:
                    ShiShix = ChuShix + math.sin(math.radians(A0 + HuanRaoShiShiJiaoDu)) * H
                    ShiShiy = ChuShiy + (HuanRaoShiShiJiaoDu - A0) / 360 * L
                    ShiShiz = ChuShiz
            elif dir.find("VER") != -1:
                ShiShix = ChuShix + (HuanRaoShiShiJiaoDu - A0) / 360 * L
                ShiShiy = ChuShiy
                ShiShiz = ChuShiz + math.sin(math.radians(A0 + HuanRaoShiShiJiaoDu)) * H
            else:
                ShiShix = ChuShix + (HuanRaoShiShiJiaoDu - A0) / 360 * L
                ShiShiy = ChuShiy + math.sin(math.radians(A0 + HuanRaoShiShiJiaoDu)) * H
                ShiShiz = ChuShiz
            self.goTo(id, [ShiShix, ShiShiy, ShiShiz])

        self.sleep(1)
        self.setAutoDelay(1)
        self.zSpeed(id, S)
        self.xySpeed(id, S)

    def WangDegYiDong(self, id, Deg, Dist, Speed):
        self.showText(id, str(id) + "号机，开始移动...")
        self.sleep(1)
        self.setAutoDelay(0)
        self.zSpeed(id, Speed)
        self.xySpeed(id, Speed)
        ChuShix = self.getFlySensor(id, "loc_x") + self.getFlySensor(id, "err_x")
        ChuShiy = self.getFlySensor(id, "loc_y") + self.getFlySensor(id, "err_y")
        ChuShiz = self.getFlySensor(id, "loc_z") + self.getFlySensor(id, "err_z")
        dx = 0.1 * Speed * math.sin(math.radians(Deg))
        dy = 0.1 * Speed * math.cos(math.radians(Deg))
        ShiShix = 0
        ShiShiy = 0
        while not math.sqrt(ShiShix * ShiShix + ShiShiy * ShiShiy) >= Dist:
            ShiShix = ShiShix + dx
            ShiShiy = ShiShiy + dy
            self.goTo(id, [ChuShix + ShiShix, ChuShiy + ShiShiy, ChuShiz])

        self.sleep(1)
        self.setAutoDelay(1)

    def WangDianYiDong(self, id, X, Y, Dist, Speed):
        dx = X - (self.getFlySensor(id, "loc_x") + self.getFlySensor(id, "err_x"))
        dy = Y - (self.getFlySensor(id, "loc_y") + self.getFlySensor(id, "err_y"))
        FangXiangJiao = math.atan2(dx, dy) * 57.29
        self.WangDegYiDong(id, FangXiangJiao, Dist, Speed)
