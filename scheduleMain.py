#%%
# import tkinter as tk
import time
import pandas as pd
from threading import Thread


#%% 
class ClockStream:

    def __init__(self, src=0):
        '''initalise the clock'''
        self.restart = False
        self.stopped = False
        self.timeNow = None
    
    def start(self):

        Thread(target=self.getTime, args=()).start()
        
        # now return the current time as a formatted string of hh:mm
        return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())  # e.g., 'Thu, weds 28 Jun 2001 14:17:15'

    def stop(self):
        '''indicate that the thread should be stopped, close the stream
        and return the duration of the programme formatted as a string'''

        self.stopped = True
        self.duration = time.time() - self.startTime

        return time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())  # e.g., 'Thu, weds 28 Jun 2001 14:17:15'



    def getTime(self):
        '''keep looping infinitely until the thread is stopped, get the time in a simple HH:MM format'''

        # maybe only update if needed to save CPU time?

        while True:
            if self.stopped:
                return
            else:
                # otherwise, read the time and save it as formatted as a string in timeNow
                self.timeNow = time.strftime("%H:%M", time.localtime())  # e.g., '14:17'

    def rtnTime(self):
        return self.timeNow

#%%
myClock = ClockStream()

startTime = myClock.start()  # init and start the clock whilst saving the full day time and date as a string in this variable

#%%
now = myClock.rtnTime()
print(now)
# %%
