#%%
# import tkinter as tk
from psychopy import visual, event, core
import time
# import pandas as pd

def startTime():
    return time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())

def getTime():
    return time.strftime("%H:%M", time.localtime())

def endTime():
    return time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()) 

# %%

win = visual.Window((1024, 768), fullscr=False, units='height', color='black')
theTimeStim = visual.TextStim(win, color='white', height=0.03, pos=(0, 0.3), text='')
circle = visual.Circle(win, edges=128, lineColor='blue', fillColor='blue', pos=(0, -0.2), radius=0.03)

while True:

    theTime = getTime()

    if theTime != theTimeStim.text:
        theTimeStim.text = theTime

    keys = event.getKeys()
    
    if keys:
        win.close()
        core.quit()
    
    theTimeStim.draw()
    circle.draw()
    win.flip()
    

