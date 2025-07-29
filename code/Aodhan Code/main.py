from machine import Pin, SPI, I2C # SPI is a class associated with the machine library. 
from machine import Timer
import time
import utime
import math

import os
import json

# The below specified libraries have to be included. Also, ssd1306.py must be saved on the Pico. 
from ssd1306 import SSD1306_SPI # this is the driver library and the corresponding class
import framebuf # this is another library for the display.

from renderer import *

# This main.py will consist of state declarations, at least a few dummy variables, and interupt declarations.
# The screen processing will be done with in the 'renderer.py' file.
# Timed interupts have some timer initialized.
# the minute counter uses tim0, and the alarm uses tim1.
# The alarm needs to be on a different timer so that it can be cancelled if the user changes the time, changes the alarm time, or turns the alarm off.

minute = 6000

state = {'vol':0,
         'freq':1013,
         '24hr':False,
         'hour':14,
         'min':53,
         'alarmHour':14,
         'alarmMin':56,
         'alarm':True,
         'invertScreen':0,
         'updated':True,
         'startup':True,
         'flash':0,
         'flashVal':0}

# Flash 0 means nothing is flashing
# 1 -> hour of clock
# 2 -> min of clock
# 3 -> hour of alarm
# 4 -> min of alarm
# 5 -> both of clock (for startup)

def loadJson():
    print("load")
    try:
        with open('stateFile.json', 'r') as file:
            temp = json.load(file)
        for key in state:
            state[key] = temp[key]
    except:
        with open('stateFile.json', 'w') as file:
            json.dump(state, file)

def saveJson():
    with open('stateFile.json', 'w') as file:
        json.dump(state, file)

if state['startup']:
    loadJson()
    state['startup'] = True
    state['flash'] = 5
    state['invertScreen'] = 0

# Starts an interupt that runs every 60 000 miliseconds, running timeUp
tim0 = machine.Timer()
# Adds 1 to the minute counter, accounting for end of hour and end of day conditions.
def timeUp(t):
    if state['flash'] == 1 or state['flash'] == 2:
        return
    state['updated'] = True
        
    state['min'] += 1
    
    if state['min'] == 60:
        state['min'] = 0
        state['hour'] += 1
        if state['hour'] == 24:
            state['hour'] = 0
    
    if state['hour'] == state['alarmHour']:
        if state['min'] == state['alarmMin']:
            alarmBlaring()
    
    saveJson()
    return

def volUp():
    state['updated'] = True
    state['vol'] += 1
    if state['vol'] > 16:
        state['vol'] = 16
    
    saveJson()
    return

def volDown():
    state['updated'] = True
    state['vol'] -= 1
    if state['vol'] < 1:
        state['vol'] = 0
    
    saveJson()
    return

def minUp():
    state['updated'] = True
    
    state['min'] += 1
    
    if state['min'] == 60:
        state['min'] = 0
        state['hour'] += 1
        if state['hour'] == 24:
            state['hour'] = 0
    
    saveJson()
    tim0.deinit()
    tim0.init(period=minute, mode=Timer.PERIODIC, callback = timeUp)
    return

def minDown():
    state['updated'] = True
    
    state['min'] -= 1
    
    if state['min'] == -1:
        state['min'] == 59
        state['hour'] -= 1
        if state['hour'] == -1:
            state['hour'] = 23
    
    saveJson()
    tim0.deinit()
    tim0.init(period=minute, mode=Timer.PERIODIC, callback = timeUp)
    return

def hourUp():
    state['updated'] = True
    
    state['hour'] += 1
    if state['hour'] == 24:
        state['hour'] = 0
    
    saveJson()
    tim0.deinit()
    tim0.init(period=minute, mode=Timer.PERIODIC, callback = timeUp)
    return

def hourDown():
    state['updated'] = True
    
    state['hour'] -= 1
    if state['hour'] == -1:
        state['hour'] = 23
    
    saveJson()
    tim0.deinit()
    tim0.init(period=minute, mode=Timer.PERIODIC, callback = timeUp)
    return

def alarmUp():
    state['updated'] = True
    
    state['alarmMin'] += 1
    
    if state['alarmMin'] == 60:
        state['alarmMin'] = 0
        state['alarmHour'] += 1
        if state['alarmHour'] == 24:
            state['alarmHour'] = 0
    
    saveJson()
    return

def alarmDown():
    state['updated'] = True
    
    state['alarmMin'] -= 1
    
    if state['alarmMin'] == -1:
        state['alarmMin'] = 59
        state['alarmHour'] -= 1
        if state['alarmHour'] == -1:
            state['alarmHour'] = 23
    
    saveJson()
    return

def aHourUp():
    state['updated'] = True
    
    state['alarmHour'] += 1
    
    if state['alarmHour'] == 24:
        state['alarmHour'] = 0
    
    saveJson()
    return

def aHourDown():
    state['updated'] = True
    
    state['alarmHour'] -= 1
    
    if state['alarmHour'] == -1:
        state['alarmHour'] = 23
    
    saveJson()
    return

def alarmToggle():
    tim2.deinit()
    state['invertScreen'] = 0
    
    if state['alarm'] is True:
        state['alarm'] = False
    else:
        state['alarm'] = True
    return
    
tim0.init(period=minute, mode=Timer.PERIODIC, callback = timeUp)

tim1 = machine.Timer() # This if for making the alarm go off

tim2 = machine.Timer() # this is for making the screen blink when the alarm goes off

tim3 = machine.Timer() # For flashing, timesetting

def flash(t):
    state['updated'] = True
    
    state['flashVal'] = 1 * (state['flashVal'] == False)
    return

tim3.init(freq=2, mode=Timer.PERIODIC, callback=flash)

def alarmSnooze():
    if (str(tim2) == "Timer(mode=PERIODIC, tick_hz=1000000, period=500000)"):
        tim2.deinit()
        state['invertScreen'] = 0
        tim1.init(period=420000, mode=Timer.ONE_SHOT, callback=alarmBlaring)
    return
    
def alarmBlaring():
    # TODO: make this do something
    state['updated'] = True
    
    tim2.init(freq=2, mode=Timer.PERIODIC, callback = invertOled)
    return
# We do not initialize the alarm here, instead we initialize it when the user sets the alarm.

def invertOled(t):
    state['updated'] = True
    
    state['invertScreen'] = 1 * (state['invertScreen'] == False)
    return

def pressClock():
    if state['24hr'] == True:
        state['24hr'] = False
    else:
        state['24hr'] = True

def knobOneC():
    if state['flash'] == 0 or state['flash'] == 5:
        volUp()
    elif state['flash'] == 1:
        hourUp()
    elif state['flash'] == 2:
        minUp()
    elif state['flash'] == 3:
        aHourUp()
    elif state['flash'] == 4:
        alarmUp()
    return

def knobOneCC():
    if state['flash'] == 0 or state['flash'] == 5:
        volDown()
    elif state['flash'] == 1:
        hourDown()
    elif state['flash'] == 2:
        minDown()
    elif state['flash'] == 3:
        aHourDown()
    elif state['flash'] == 4:
        alarmDown()
    return

def knobOnePress():
    if state['flash'] < 4:
        state['flash'] += 1
    if state['flash'] == 4:
        state['flash'] = 0
    if state['flash'] == 5:
        state['flash'] = 1

def knobTwoC():
    state['freq'] += 2
    if state['freq'] == 1082:
        state['freq'] = 880
    return

def knobTwoCC():
    state['freq'] -= 2
    if state['freq'] == 878:
        state['freq'] = 1080
    return



# Main rendering loop
while(True):
    # Do things
    if(state['updated']):
        render(state)
        state['updated'] = False