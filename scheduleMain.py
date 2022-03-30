#%%
from fileinput import filename
from psychopy import visual, event, gui, core
from datetime import datetime, timedelta
import time
import pandas as pd
from pathlib import Path

## TODO
# Sound When Due
#### Maybe a grating bottom right to show active 


JUST_DATE = "%d/%m/%Y"
FULL_DATETIME = "%d/%m/%Y %H:%M:%S"
FULL_TIME = "%H:%M:%S"
SHORT_TIME = "%H:%M"

ILLEGAL_KEYS = ['insert', 'delete', 'right', 'left', 'up', 'down', 'pageup',
                'pagedown', 'home', 'end', 'capslock', 'scrolllock', 'numlock',
                'printscreen', 'pause', 'f1', 'f2', 'f3', 'f4', 'f5',
                'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12', 'bracketleft',
                'bracketright', 'lshift', 'rshift', 'lctrl', 'rctrl', 'lalt',
                'ralt', 'menu', 'semicolon', 'minus', 'equal', 'windows',
                'apostrophe', 'quoteleft', 'pound', 'lwindows', 'lwindow']
#%% Functions
class taskDispatcher:

    def __init__(self, taskList):

        self.taskList = taskList
        self.totalTasks = len(self.taskList)
        self.dynamicTaskList = taskList  # Only interact with this 
        self.tasksComplete = 0
        self.allTasksComplete = False

    def getNextTask(self):
        '''Returns a dictionary of the datetime and string values for
           the next task display
           
           PARAMETERS
           
           '''
        self.remainingTaskList = self.dynamicTaskList

        if not self.allTasksComplete:

            self.nextTaskDict = self.remainingTaskList.pop(0)
            self.dynamicTaskList = self.remainingTaskList  # to update the actual variable minus 1
            return (self.nextTaskDict)


    def taskLogComplete(self, fileName, taskDetailsDict):
        '''The main logging function to timestamp, mark complete and write to file
        
           PARAMETERS:
           fileName: Str/Path file path of the filename
           taskDetailsDict: the dictionary returned by getNextTask with the notes!  
        '''

        timeStamp = datetime.now().strftime(FULL_DATETIME)
        day = taskDetailsDict['day']
        scheduledTime = taskDetailsDict['scheduledTime']
        task = taskDetailsDict['task']
        rqrUsrInput = taskDetailsDict['usrInput']
        taskNotes =  taskDetailsDict['taskNotes']  
        
        with open(fileName, mode='a') as f:
            dataWriter(f, [day, scheduledTime, task, rqrUsrInput, taskNotes, timeStamp])

        self.tasksComplete += 1
        
        if self.totalTasks == self.tasksComplete:
            self.allTasksComplete = True
        
        return True 



def calcScreenWidth(windowXY):
    '''Helper function that returns the width of the screen in height units.
       This returns the /2 in that you can infer +/- directly from the
       returned value. For example, you can use the value to say img.pos= -[val]
    '''
    screenWidth = windowXY[0] / windowXY[1] / 2

    return screenWidth

def imgSizer(newY, oldHeight, oldWidth):
    '''Helper function to calculate new relative width of an image
       dependent on the new newY (between 0.001-1.0).

       This is designed for use with 'height' as the unit method in PsychoPy,
       and so returns sizes as floats.

       the newY value needs to be between 0.001-1.0 for use with "Height"
       units.

       PARAMETERS:
       newY:            Either newWidth if X, or newHeight if Y
       oldHeight:       Original Height in Height units
       oldWidth:        Original Width in Height units
    '''

    # # Wakes formula for conversion
    # imgX, imgY = (576, 1024)
    # newY = 0.8  # 80% of the screen in height units
    # newX = newY * imgX / imgY

    resizedVal = newY * oldWidth / oldHeight
    newSize = (resizedVal, newY)

    return newSize

def dataWriter(fileName, parameterList, delim='\t'):
    '''Provides an easy function that writes deliminated data
        
        PARAMETERS
        fileName: Should be a file object in w or a mode
        parameterList: A list of items to write 
        delim: string. By default it assumes tab delimination, but can be any delim (e.g., ',') 
    '''
    for item in enumerate(parameterList):
        fileName.write(str(item[1]))
        if item[0] != (len(parameterList)-1):
            fileName.write(delim)
    fileName.write('\n')
    return 1

def isDir(pth):
    '''Checks if Path object is a directory or not, and creates as necessary.
    
        PARAMETERS:
        pth: a Path object
        
        '''
    if pth.is_dir():
        print('Directory Exists, Passing...')
        pass
    else:
        print("Directory Does Not Exist, Creating")
        pth.mkdir(parents=True, exist_ok=False)
    return pth

def taskDisplayFormatter(lstOfDictTasks):
    '''Simply creates a string formatted table
    
    TODO: needs to solve for dates
    
    '''
    formattedStr = 'ScheduledTime    Task\n\n'
    for task in lstOfDictTasks:
        formattedStr = formattedStr + f"  {task['scheduledTime']}          {task['task']}\n"
    return formattedStr

def daySolver(dayLst):
    '''This function should solve how many days 
       are in the schedule and assign them a real 
       date.
       
       PARAMETERS
       dayLst: should be a simple list of int of every day number
               in the day column, 1 being the first'''

    dateDict = {}
    startDate = datetime.now().date()

    # this should be difference in days from day 1, not day number
    # so day-1, not just day in timedelta
    for day in dayLst:
        if day == 1:
            dateDict[day] = startDate
        else:
            dateDict[day] = startDate + timedelta(days=day-1)

    return dateDict

def timeChecker(nextTaskDateTime):
    '''A function that checks whether the time for the next task
       is due
    
       PARAMETERS
       nextTaskDateTime: This should be a complete datetime object'
    
       RETURNS simple True or False that the task is due, even if it overdue
    '''
    if isinstance(nextTaskDateTime, str):
        return False
    
    now = datetime.now().replace(second=0, microsecond=0)

    if now <= nextTaskDateTime:  # if now is before the task time
        return False
    elif now >= nextTaskDateTime:
        return True
    else:
        print("DEBUG timeChecker")


#%% Solve the DataFrame date stuff
df = pd.read_excel('schedule.xlsx')
# first lets solve the date by adding a new column based on the day column
dayMap = daySolver(df['day'].tolist())
df['date'] = df['day'].map(dayMap)  # adds these as a datetime.date
# create a final Col that combines the dates and times
df['dateTimeObj'] = df.apply(lambda df : pd.datetime.combine(df['date'],df['scheduledTime']), axis=1)

#%%

# Participant Info and Other Settings
info = {}
info['participant'] = ''
info['age'] = ''
info['sex'] = ['Female', 'Male', 'Other', 'Prefer Not To Say']
info['studyName'] = ''

dlg = gui.DlgFromDict(info)  # dialog box
if not dlg.OK:  # did they push ok?
    core.quit()

# Debug info dict
# info = {'participant': 'Kris', 'age': 33, 'sex': 'Male', "studyName": 'Test Study'}

# Working Directory and Output File path
WD = Path.cwd()
fileTime = time.strftime("%d-%m-%Y_%H-%M-%S", time.localtime())
outputFile = WD / f"{info['participant']}_{fileTime}.csv"

headers = ['day', 'scheduledTime', 'taskName', 'usrInput', 'taskNotes', 'loggedCompleteTime']
with open(outputFile, mode='w') as f:
    f.write(f"Study Name: {info['studyName']}\nParticipant: {info['participant']}\nSex: {info['sex']}\nAge: {info['age']}\n\n")
    dataWriter(f, headers)


# %%
win = visual.Window((1920, 1080), fullscr=False, units='height', color='black')
winSizeX = calcScreenWidth(win.size)  # returns an float(x)
northumbriaLogo = visual.ImageStim(win, image='img/unn2.png', pos=(0, 0.36))
currentDateTextStim = visual.TextStim(win, color='white', height=0.05, pos=(winSizeX/1.55, 0.4), text='')
currentTimeTextStim = visual.TextStim(win, color='white', height=0.08, pos=(winSizeX/1.55, 0.33), text='')
partStudyTextStim = visual.TextStim(win, color='white', height=0.03, pos=(0, 0.15), text='')
nextTaskTextStim = visual.TextStim(win, color='white', height=0.05, pos=(0, -0.15), text='')
# upcomingListTextStim = visual.TextStim(win, color='white', height=0.03, pos=(-(winSizeX/1.3), 0.2), text='', anchorHoriz='left', anchorVert='top', wrapWidth=None)
upcomingListTextStim = visual.TextBox2(win, font='Open Sans', color='white', letterHeight=0.02, pos=(-(winSizeX/2.6), 0.2), text='', editable=False)
taskBox = visual.Rect(win, pos=(0, -0.15), size=(winSizeX/1.2,winSizeX/2))
userInputTextStim = visual.TextStim(win, color='white', height=0.05, pos=(0, -0.32), text='')
screenUpdateClock = core.CountdownTimer(start=10)

#%% Prelim
run = True
taskManager = taskDispatcher(df.to_dict('records'))  # list of dict
# print('dynamic Task List')
# print(taskManager.dynamicTaskList)  # Seems ok here
pullNextTask = True
currentTaskComplete = False

remainingTasks = taskManager.dynamicTaskList
remainingTaskDisplay = taskDisplayFormatter(remainingTasks)

userLog = []

# get some values to start
now = datetime.now()
dateNow = now.strftime(JUST_DATE)
timeNow = now.strftime(SHORT_TIME)
participantStudyText = f"Study: {info['studyName']}\nParticipant: {info['participant']}"
partStudyTextStim.text = participantStudyText

#%% Main Run 
screenUpdateClock.reset()
while run:

    if screenUpdateClock.getTime() <= 0:
        # every time the clock gets to 0
        # Update values for the clock, date
        now = datetime.now()
        dateNow = now.strftime(JUST_DATE)
        timeNow = now.strftime(SHORT_TIME)
        screenUpdateClock.reset()

    # Apply them and draw them

    # Date
    if currentDateTextStim.text != dateNow:
        currentDateTextStim.text = dateNow
    currentDateTextStim.draw()

    # Time
    if currentTimeTextStim.text != timeNow:
        currentTimeTextStim.text = timeNow
    currentTimeTextStim.draw()

    # Study/Part/Logo
    partStudyTextStim.draw()
    northumbriaLogo.draw()

    # Now Deal with the Task Stuff
    # Maybe a function that deals with all this stuff?
    
    if pullNextTask and not taskManager.allTasksComplete:
        currentTaskAtHand = taskManager.getNextTask()
        print(currentTaskAtHand)
        pullNextTask = False
        
        taskWhen = currentTaskAtHand['dateTimeObj']
        writeData = True

        if currentTaskAtHand['usrInput'] == 'yes':
            taskInput = "\nType Log Message\nthen Press Enter"
            needLog = True
        elif currentTaskAtHand['usrInput'] == 'no':
            taskInput = "\nPress Enter to Log"
            needLog = False

    elif taskManager.allTasksComplete:
        currentTaskAtHand = 'complete'
        taskWhen = ''
        taskInput = 'Press Q to quit'
        needLog = False
        writeData = False

    # Set up the other variables
    if not isinstance(taskWhen, str): 
        taskText = f"{taskWhen.strftime(SHORT_TIME)}\n{currentTaskAtHand['task']}\n{taskInput}"  

    elif isinstance(taskWhen, str):
        taskText = "All Tasks Complete\nPress Q to Quit"

    if nextTaskTextStim.text != taskText:
        nextTaskTextStim.text = taskText
    nextTaskTextStim.draw()

    if timeChecker(taskWhen) is False:
        taskBox.lineColor = 'green'
    elif timeChecker(taskWhen) is True:
        taskBox.lineColor = 'red'
    taskBox.draw()

    # Sort the task list (Left pane)
    remainingTasks = taskManager.dynamicTaskList
    remainingTaskDisplay = taskDisplayFormatter(remainingTasks)
    if upcomingListTextStim.text != remainingTaskDisplay:
        upcomingListTextStim.text = remainingTaskDisplay
    upcomingListTextStim.draw()
    
   # Listen for Keys / Add KeyLogger currentTaskComplete Switch
    # deal with input 
    keys = event.getKeys()
    acceptLog = False
    if len(keys) > 0 and needLog:

        if keys[0] == 'return' or keys[0] == 'enter':
            if len(userLog) == 0:
                pass
            elif len(userLog) > 0:
                currentTaskAtHand['taskNotes'] = ''.join(userLog)
                taskManager.taskLogComplete(outputFile, currentTaskAtHand)

                pullNextTask = True
                acceptLog = True
                userLog = []
                      
        elif keys[0] == 'escape':
            pass  # Build in quit!?
        elif keys[0] in ILLEGAL_KEYS:
            pass
        elif keys[0] == 'backspace':
            try:
                del userLog[-1]
            except IndexError:
                pass
        elif keys[0] == 'comma':
            userLog.append(',')
        elif keys[0] == 'period':
            userLog.append('.')
        elif keys[0] == 'backslash':
            userLog.append('//')
        elif keys[0] == 'space':
            userLog.append(' ')
        elif keys[0] == 'tab':
            userLog.append('    ')
        elif keys[0] == 'minus':
            userLog.append('-')
        elif keys[0] == 'semicolon':
            userLog.append(';')
        else:
            userLog.append(keys[0])

    elif len(keys) > 0 and not needLog:
        if keys[0] in ['return', 'enter', 'q']:
            userLog.append('N/A')

            if keys[0] == 'q' and taskManager.allTasksComplete:
                win.close()
                core.quit()

            if isinstance(currentTaskAtHand, dict):
                currentTaskAtHand['taskNotes'] = ''.join(userLog)

            if writeData:
                taskManager.taskLogComplete(outputFile, currentTaskAtHand)
            
            acceptLog = True
            pullNextTask = True
            userLog = []
            

    userInputTextStim.text = ''.join(userLog)
    userInputTextStim.draw()

    win.flip()

