import tkinter as tk
import datetime
import time
import pandas as pd
from threading import Thread



# time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
# # 'Thu, 28 Jun 2001 14:17:15'



class ClockStream:

    def __init__(self, src=0):
        '''initalise the clock and read the time'''
        self.startTime = time.time()
        self.restart = False
        self.stopped = False
    
    def start(self):

        Thread(target=self.getTime, args=()).start()
        # now return it as a formatted string of hh:mm

    def stop(self):
        '''indicate that the thread should be stopped, close the stream
        and return the duration of the programme formatted as a string'''

        self.stopped = True
        self.duration = time.time() - self.startTime
        # format the duration and retunr it as a formatted string of hh:mm:ss


    def getTime(self):
        '''keep looping infinitely until the thread is stopped'''

        # maybe only update if needed to save CPU time?

        while True:
            if self.stopped:
                return
            else:
                # otherwise, read the time and return it formatted as a string
                pass