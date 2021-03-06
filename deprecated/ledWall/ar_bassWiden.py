#!/usr/bin/env python

import numpy as np
import sys
sys.path.append("../ar/")
import fastopc, time
import functionLib as lib
import micStream

if len(sys.argv) == 1: brightnessFactor = 0.6
else: brightnessFactor = float(sys.argv[1])

nStrips = 16
lStrip  = 64
client = fastopc.FastOPC('localhost:7890')

pixels    = lib.Pixels(nStrips, lStrip, 0)
theoStrip = np.zeros([lStrip, 3])
theo      = np.zeros([nStrips*lStrip, 3])

stream = micStream.Stream(fps=30, nBuffers=4)

powerSmooth = lib.ExpFilter(val=0.05, alpha_rise=0.05, alpha_decay=0.05)
nColorWheel = 600
colorWheel = lib.getColorWheel(nColorWheel)
frameCount = 0

while True:
    success = stream.readAndCalc()
    if success:
        frameNumEff = np.mod(frameCount, nColorWheel)
        power = np.sum(stream.freqSpectrum[20//7:250//7])
        powerSmooth.update(power)
        displayPower = int(122*power/powerSmooth.value)
        width = int(5 + np.sqrt(float(displayPower)))
        for i in range(8):
            theoStrip[width:] = displayPower * colorWheel[np.mod(frameNumEff+10*i+200,nColorWheel)]
            theoStrip[0:width] =  255 * colorWheel[np.mod(frameNumEff+10*i,nColorWheel)]
            theo[(2*i+0)*lStrip:(2*i+1)*lStrip] = theoStrip
            theo[(2*i+1)*lStrip:(2*i+2)*lStrip] = theoStrip
        pixels.update(theo, 0.7, 0.1)
        #print(width)
        #print(displayPower * colorWheel[frameNumEff])
        client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        frameCount+=1
