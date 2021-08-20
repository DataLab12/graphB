from datetime import datetime
from functools import reduce
 

class Timer:

    timerNumber = None
    startTime = None
    stopTime = None
    elapsedTime = None
    timerName = None

    def __init__(self, index, name):
        self.timerNumber = index
        self.timerName = name
        self.allElapsedTimes = []
   
    def start(self):
        if self.startTime is None:
            self.startTime = datetime.now()
            self.elapsedTime = None

    def stop(self):
            self.stopTime = datetime.now()
            self.elapsedTime = self.stopTime - self.startTime
            self.allElapsedTimes.append(self.elapsedTime)
            self.startTime = None
            self.stopTime = None
               
    def getElapsedTime(self):
            return self.elapsedTime

    def getAverageTime(self):
            sumTimes = reduce(lambda x, y: x + y, self.allElapsedTimes)
            return sumTimes/len(self.allElapsedTimes)

    def getSumTime(self):
            sumTimes = reduce(lambda x, y: x + y, self.allElapsedTimes) 
            return sumTimes
            
    def getAllTimes(self):
        print(self.allElapsedTimes)

        
