#!/usr/bin/env python

import numpy as np
import sys
sys.path.append("../ar/")
import fastopc, time
import functionLib as lib
import micStream

if len(sys.argv) == 1: brightnessFactor = 0.6
else: brightnessFactor = float(sys.argv[1])

client = fastopc.FastOPC('localhost:7890')

lNeck  = 18
lBody  = 40
lStrap = 36

pixels    = lib.BassPixels(lNeck, lBody, lStrap, 0)
theoNeck  = np.zeros([lNeck,  3])
theoBody  = np.zeros([lBody,  3])
theoStrap = np.zeros([lStrap, 3])

stream = micStream.Stream(fps=30, nBuffers=4)

powerSmooth = lib.ExpFilter(val=0.05, alpha_rise=0.05, alpha_decay=0.05)
nColorWheel = 600
colorWheel = lib.getColorWheel(nColorWheel)
frameCount = 0

breakVar=0
while breakVar==0:
    success = stream.readAndCalc()
    if success:
        frameNumEff = np.mod(frameCount, nColorWheel)
        power = np.sum(stream.freqSpectrum[20//7:250//7])
        powerSmooth.update(power)
        displayPower = int(122*np.power(power/powerSmooth.value, 1.5))
        theoNeck     = np.roll(theoNeck, 1, axis=0)
        theoNeck[0]  = displayPower * colorWheel[frameNumEff]
        theoBody     = displayPower * colorWheel[np.mod(frameNumEff+200, nColorWheel)]
        pixels.updateBody(theoBody, 0.5, 0.5)
        pixels.updateNeck(theoNeck, 0.5, 0.5)
        print(displayPower * colorWheel[frameNumEff])
        #client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        frameCount+=1
