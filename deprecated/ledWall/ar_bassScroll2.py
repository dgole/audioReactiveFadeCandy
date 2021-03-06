#!/usr/bin/env python

import numpy as np
import sys
sys.path.append("../ar/")
import fastopc, time
import functionLib as lib
import micStream

nStrips = 16
lStrip  = 64

if len(sys.argv) == 1: brightnessFactor = 0.6
else: brightnessFactor = float(sys.argv[1])

client = fastopc.FastOPC('localhost:7890')

pixels    = lib.Pixels(nStrips, lStrip, 0)
theo      = np.zeros([nStrips*lStrip, 3])

stream = micStream.Stream(fps=30, nBuffers=4)

powerSmooth = lib.ExpFilter(val=0.05, alpha_rise=0.01, alpha_decay=0.01)
nColorWheel = 300
colorWheel = lib.getColorWheel(nColorWheel)
frameCount = 0

while True:
    success = stream.readAndCalc()
    if success:
        frameNumEff = np.mod(frameCount, nColorWheel)
        power = np.sum(stream.freqSpectrum[20//7:250//7])
        powerSmooth.update(power)
        displayPower = int(122*np.power(power/powerSmooth.value,1.5))
        theo = np.roll(theo, 128, axis=0)
        theo[0:128] = displayPower * colorWheel[frameNumEff]
        pixels.update(theo, 0.7, 0.2)
        #print(displayPower * colorWheel[frameNumEff])
        client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        frameCount+=1
