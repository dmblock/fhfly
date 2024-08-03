from helloFly import fly

fh = fly()

def getTicks_sec():
    fh.getTicks_sec()

def getTimer():
    fh.getTimer()

def clearTimer():
    fh.clearTimer()

def pyLink_pack(fun, buff):
    fh.pyLink_pack(fun, buff)

def sendOrderPack(id, cmd, pack):
    fh.sendOrderPack(id, cmd, pack)

def sleep(sec):
    fh.sleep(sec)

def setAutoDelay(auto):
    fh.setAutoDelay(auto)

def tts(string, wait=True):
    fh.tts(string, wait=True)

def moveDelay(id):
    fh.moveDelay(id)

def autoDelay(sec):
    fh.autoDelay(sec)

def takeOff(id, high):
    fh.takeOff(id, high)

def flyCtrl(id, mode):
    fh.flyCtrl(id, mode)

def flyMode(id, mode):
    fh.flyMode(id, mode)

def zSpeed(id, speed):
    fh.zSpeed(id, speed)

def move(id, mode, loc):
    fh.move(id, mode, loc)

def moveSearchBlob(id, dir, distance, blob):
    fh.moveSearchBlob(id, dir, distance, blob)

def moveSearchTag(id, dir, distance, tagID):
    fh.moveSearchTag(id, dir, distance, tagID)

def moveFollowTag(id, dir, distance, tagID):
    fh.moveFollowTag(id, dir, distance, tagID)

def goTo(id, loc):
    fh.goTo(id, loc)

def goToTag(id, tagID, high):
    fh.goToTag(id, tagID, high)

def moveByAngle(id, Deg, Dist, Speed):
    fh.moveByAngle(id, Deg, Dist, Speed)

def moveToPoint(id, X, Y, Dist, Speed):
    fh.moveToPoint(id, X, Y, Dist, Speed)
