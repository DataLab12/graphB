from Timer import Timer

class TimerManager:

    timers = []
    timerCount = 0
    __instance = None

    @staticmethod
    def getInstance():
        if TimerManager.__instance is None:
            TimerManager()
        return TimerManager.__instance

    def __init__(self):
        if TimerManager.__instance is None:
            TimerManager.__instance = self
        else:
            print("TimerManager already made.")

    @staticmethod
    def addTimer(name):
        TimerManager.timers.append(Timer(TimerManager.timerCount, name))
        TimerManager.timerCount += 1

    @staticmethod
    def startTimerX(index):
        try:
            timer = TimerManager.timers[index]
            timer.start()
        except IndexError:
            print("Timer selection out of bounds. Max timer index is {}".format(TimerManager.timerCount - 1))

    @staticmethod
    def stopTimerX(index):
        try:
            timer = TimerManager.timers[index]
            timer.stop()
        except IndexError:
            print("Timer selection out of bounds. Max timer index is {}".format(TimerManager.timerCount - 1))

    @staticmethod
    def getTimerXStart(index):
        try:
            timer = TimerManager.timers[index]
            return timer.startTime
        except IndexError:
            print("Timer selection out of bounds. Max timer index is {}".format(TimerManager.timerCount - 1))
    
    @staticmethod
    def getTimerXElapsed(index):
        try:
            timer = TimerManager.timers[index]
            return timer.getElapsedTime()
        except IndexError:
            print("Timer selection out of bounds. Max timer index is {}".format(TimerManager.timerCount - 1))

    @staticmethod
    def getTimerXName(index):
        try:
            timer = TimerManager.timers[index]
            return timer.timerName
        except IndexError:
            print("Timer selection out of bounds. Max timer index is {}".format(TimerManager.timerCount - 1))

    @staticmethod
    def getTimerXAvg(index):
        try:
            timer = TimerManager.timers[index]
            return timer.getAverageTime()
        except IndexError:
            print("Timer selection out of bounds. Max timer index is {}".format(TimerManager.timerCount - 1))
    
    @staticmethod
    def getTimerXSum(index):
        try:
            timer = TimerManager.timers[index]
            return timer.getSumTime()
        except IndexError:
            print("Timer selection out of bounds. Max timer index is {}".format(TimerManager.timerCount - 1))

    @staticmethod
    def removeTimer(index):
        try:
            TimerManager.timers.remove(index)
        except IndexError:
            print("Timer selection out of bounds. Max timer index is {}".format(TimerManager.timerCount - 1))
