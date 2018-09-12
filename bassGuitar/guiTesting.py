import numpy as np
import sys
sys.path.append("../ar/")
import fastopc, time
import functionLib as lib
import micStream
import bassGuitarPatterns as patterns
import Tkinter as tkinter

brightnessFactor = 0.7

def placePatternButtons(brightnessFactor):
    tkinter.Button(window1, text='basic', command=lambda a=brightnessFactor: patterns.basic(a)).grid(row=8+0, column=1, sticky='W')
    tkinter.Button(window1, text='scroll', command=lambda a=brightnessFactor: patterns.scroll(a)).grid(row=8+1, column=1, sticky='W')

def changeBrightness(i):
    brightnessFactor = float(i)/10.0
    lbl3.configure(text='current brightness is ' + str(float(i)/10.0))
    placePatternButtons(brightnessFactor)

window1 = tkinter.Tk()
window1.geometry("600x800")
window1.title("AUDIO REACTIVE LEDs!")

tkinter.Label(window1, text='1. click button for brightness \n').grid(row=0, column=0, sticky='W')
tkinter.Label(window1, text='2. click button for pattern \n').grid(row=1, column=0, sticky='W')
tkinter.Label(window1, text='3. to stop a currently running program').grid(row=2, column=0, sticky='W')
tkinter.Label(window1, text='   click the terminal window and press cntrl+c        \n').grid(row=3, column=0, sticky='W')
tkinter.Label(window1, text='4. to start another program').grid(row=4, column=0, sticky='W')
tkinter.Label(window1, text='   select the brightness and another program       \n \n').grid(row=5, column=0, sticky='W')

############# PATTERN ################
lbl2 = tkinter.Label(window1, text='select pattern below')
lbl2.grid(row=7, column=1, sticky='W')

placePatternButtons(brightnessFactor)

############# BRIGHTNESS ################
lbl3 = tkinter.Label(window1, text='current brightness is none')
lbl3.grid(row=6, column=0, sticky='W')

lbl4 = tkinter.Label(window1, text='select brightness below')
lbl4.grid(row=7, column=0, sticky='W')

for i in range(11):
    tkinter.Button(window1, text=str(float(i)/10.0), command=lambda n=i: changeBrightness(n)).grid(row=8+i, column=0, sticky='W')


window1.mainloop()
