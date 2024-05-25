# uncompyle6 version 3.9.1
# Python bytecode version base 3.6 (3379)
# Decompiled from: Python 3.12.2 (tags/v3.12.2:6abddd9, Feb  6 2024, 21:26:36) [MSC v.1937 64 bit (AMD64)]
# Embedded file name: flyData.py
# Compiled at: 2024-02-25 10:20:34
# Size of source mod 2**32: 4773 bytes
from struct import unpack

class mv_t(object):
    flag = 0
    tagId = 0
    blob_n = 0
    blob_s = 0
    blob_w = 0
    blob_h = 0


class sensor(object):
    id = 0
    vol = 0
    ssi = 0
    state = 0
    obs_dist = [255, 255, 255, 255]
    imu = [0, 0, 0]
    loc = [0, 0, 0]
    locErr = [0, 0, 0]
    sys_flag = 0
    laserTarget_count = 0
    laserTarget_result = 0
    laserTarget_x = 0
    laserTarget_y = 0
    scale_weight = 0
    newsCount = 0
    newsLen = 0
    news = ""
    qrCode = ""
    brCode = ""
    mv = mv_t()


class photo_t(object):
    id = 0
    isOk = False


class init:

    def __init__(self, flyNum):
        self.maxNum = 10
        self.flySensor = [sensor() for _ in range(self.maxNum)]
        self.keyPressId = 255
        self.photo = photo_t()

    def getKey(self, aux4, aux5):
        for i in range(16):
            if aux4 & 1 << i:
                return i

        if aux5 & 255:
            return 16
        else:
            if aux5 & 65280:
                return 17
            return 255

    def Receive_Anl(self, rx):
        if rx.date[0] == 1:
            pack = unpack("<3BHB4B6h3b", bytearray(rx.date)[1:rx.len])
            id = pack[0]
            if id < self.maxNum:
                self.flySensor[id].id = pack[0]
                self.flySensor[id].vol = pack[1] * 0.1
                self.flySensor[id].ssi = pack[2]
                self.flySensor[id].state = pack[3]
                self.flySensor[id].sys_flag = pack[4]
                self.flySensor[id].obs_dist = [pack[5], pack[6], pack[7], pack[8]]
                self.flySensor[id].imu = [pack[9] * 0.1, pack[10] * 0.1, pack[11] * 0.1]
                self.flySensor[id].loc = [pack[12], pack[13], pack[14]]
                self.flySensor[id].locErr = [pack[15], pack[16], pack[17]]
                if self.photo.id == id:
                    self.photo.isOk = True if self.flySensor[id].sys_flag & 1 else False
        elif rx.date[0] == 14:
            pack = unpack("<2BHBL2H", bytearray(rx.date)[1:rx.len])
            id = pack[0]
            if id < self.maxNum:
                self.flySensor[id].mv.flag = pack[1]
                self.flySensor[id].mv.tagId = pack[2]
                self.flySensor[id].mv.blob_n = pack[3]
                self.flySensor[id].mv.blob_s = pack[4]
                self.flySensor[id].mv.blob_w = pack[5]
                self.flySensor[id].mv.blob_h = pack[6]
        elif rx.date[0] == 2:
            pass
        pack = unpack("<4B2h4Bf", bytearray(rx.date)[1:rx.len])
        id = pack[0]
        if id < self.maxNum:
            self.flySensor[id].id = pack[0]
            self.flySensor[id].ssi = pack[1]
            self.flySensor[id].laserTarget_count = pack[2]
            self.flySensor[id].laserTarget_result = pack[3]
            self.flySensor[id].laserTarget_x = pack[4]
            self.flySensor[id].laserTarget_y = pack[5]
            self.flySensor[id].obs_dist = [pack[6], pack[7], pack[8], pack[9]]
            self.flySensor[id].scale_weight = pack[10]
        else:
            if rx.date[0] == 244 or rx.date[0] == 245 or rx.date[0] == 246 or rx.date[0] == 255:
                pack = unpack("<3B", bytearray(rx.date)[1:4])
                id = pack[0]
                if self.flySensor[id].newsCount == pack[1]:
                    return
        if id < self.maxNum:
            self.flySensor[id].id = pack[0]
            self.flySensor[id].newsCount = pack[1]
            self.flySensor[id].newsLen = pack[2]
            try:
                news = bytearray(rx.date)[4:4 + pack[2]].decode("utf-8")
            except:
                news = "UnicodeError"

            if rx.date[0] == 244:
                self.flySensor[id].qrCode = news
                print(str(id) + "号(二维码)：" + news)
            elif rx.date[0] == 245:
                self.flySensor[id].brCode = news
                print(str(id) + "号(条形码)：" + news)
            elif rx.date[0] == 246:
                self.flySensor[id].news = news
                print(str(id) + "号(消息)：" + news)
            else:
                print(str(id) + "号(提示)：" + news)
        elif rx.date[0] == 3:
            pack = unpack("<10H2BI", bytearray(rx.date)[1:rx.len])
            self.keyPressId = self.getKey(pack[7], pack[8])
