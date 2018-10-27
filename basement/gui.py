import numpy as np
import sys
sys.path.append("../ar/")
import fastopc, time
import functionLib as lib
import micStream
import basementPatterns as patterns
import Tkinter as tk

brightnessFactor = 0.7 # default brightness factor

def placePatternButtons(brightnessFactor):
    ''' define function that places the pattern buttons with the
        current brightnessFactor '''
    tk.Button(window1, text='chase', command=lambda a=brightnessFactor: patterns.chase(a)).grid(row=8+0, column=1, sticky='W')
    tk.Button(window1, text='bouncers', command=lambda a=brightnessFactor: patterns.bouncers(a)).grid(row=8+1, column=1, sticky='W')
    tk.Button(window1, text='stars', command=lambda a=brightnessFactor: patterns.stars(a)).grid(row=8+2, column=1, sticky='W')
    tk.Button(window1, text='bassWiden', command=lambda a=brightnessFactor: patterns.bassWiden(a)).grid(row=8+3, column=1, sticky='W')
    tk.Button(window1, text='bassScrollMiddle', command=lambda a=brightnessFactor: patterns.bassScrollMiddle(a)).grid(row=8+4, column=1, sticky='W')
    tk.Button(window1, text='bassScrollTop', command=lambda a=brightnessFactor: patterns.bassScrollTop(a)).grid(row=8+5, column=1, sticky='W')
    tk.Button(window1, text='beatDetection', command=lambda a=brightnessFactor: patterns.beatDetection(a)).grid(row=8+6, column=1, sticky='W')
    tk.Button(window1, text='bouncers_ar', command=lambda a=brightnessFactor: patterns.bouncers_ar(a)).grid(row=8+7, column=1, sticky='W')
    tk.Button(window1, text='chase_beatDetection', command=lambda a=brightnessFactor: patterns.chase_beatDetection(a)).grid(row=8+8, column=1, sticky='W')
    tk.Button(window1, text='rain1', command=lambda a=brightnessFactor: patterns.rain1(a)).grid(row=8+9, column=1, sticky='W')
    tk.Button(window1, text='rain2', command=lambda a=brightnessFactor: patterns.rain2(a)).grid(row=8+10, column=1, sticky='W')
    tk.Button(window1, text='rain1_midi', command=lambda a=brightnessFactor: patterns.rain1_midi(a)).grid(row=8+11, column=1, sticky='W')
    tk.Button(window1, text='rain2_midi', command=lambda a=brightnessFactor: patterns.rain2_midi(a)).grid(row=8+12, column=1, sticky='W')


def changeBrightness(i):
    ''' function that gets called when a brigntess button gets pressed
        change the brightness factor, change displayed brightnessFactor,
        replace the pattern buttons based on the current brightnessFactor '''
    brightnessFactor = float(i)/10.0
    lbl3.configure(text='current brightness is ' + str(float(i)/10.0))
    placePatternButtons(brightnessFactor)

# make the window
window1 = tk.Tk()
window1.geometry("600x800")
window1.title("AUDIO REACTIVE LEDs!")

# print instructions in window
tk.Label(window1, text='1. click button for brightness \n').grid(row=0, column=0, sticky='W')
tk.Label(window1, text='2. click button for pattern \n').grid(row=1, column=0, sticky='W')
tk.Label(window1, text='3. to stop a currently running program').grid(row=2, column=0, sticky='W')
tk.Label(window1, text='   click the terminal window and press cntrl+c        \n').grid(row=3, column=0, sticky='W')
tk.Label(window1, text='4. to start another program').grid(row=4, column=0, sticky='W')
tk.Label(window1, text='   select the brightness and another program       \n \n').grid(row=5, column=0, sticky='W')

# pattern selection
lbl2 = tk.Label(window1, text='select pattern below')
lbl2.grid(row=7, column=1, sticky='W')
placePatternButtons(brightnessFactor)

# brightness selection
lbl3 = tk.Label(window1, text='current brightness is ' + str(0.7))
lbl3.grid(row=6, column=0, sticky='W')
lbl4 = tk.Label(window1, text='select brightness below')
lbl4.grid(row=7, column=0, sticky='W')
for i in range(11):
    tk.Button(window1, text=str(float(i)/10.0), command=lambda n=i: changeBrightness(n)).grid(row=8+i, column=0, sticky='W')

# enter main loop of gui
window1.mainloop()
