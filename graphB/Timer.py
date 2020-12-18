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
        else:
            print("This timer has already been started.")

    def stop(self):
        if self.startTime is None:
            print("This timer hasn't been started yet.")
#        elif self.stopTime is not None:
#            print("This timer has already been stopped.")
        else:
            self.stopTime = datetime.now()
            self.elapsedTime = self.stopTime - self.startTime
            self.allElapsedTimes.append(self.elapsedTime)
            self.startTime = None
            self.stopTime = None
               
    def getElapsedTime(self):
        if self.startTime is not None:
            print("This timer is currently running and must be stopped first")
        if self.stopTime is not None:
            print("This timer hasn't been stopped")
        else:
            return self.elapsedTime

    def getAverageTime(self):
        if self.startTime is not None:
            print("This timer is still running and must be stopped first")
        elif self.stopTime is not None:
            print("This timer hasn't been stopped")
        else:
            sumTimes = reduce(lambda x, y: x + y, self.allElapsedTimes)
            return sumTimes/len(self.allElapsedTimes)

    def getSumTime(self):
        if self.startTime is not None:
            print("This timer is still running and must be stopped first")
        elif self.stopTime is not None:
            print("This timer hasn't been stopped")
        else:
            sumTimes = reduce(lambda x, y: x + y, self.allElapsedTimes) 
            return sumTimes
            
    def getAllTimes(self):
        print(self.allElapsedTimes)

        
