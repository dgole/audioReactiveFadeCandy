#!/usr/bin/env python

import fastopc, time
import numpy as np
import functionLib as lib
import micStream

nStrips = 16
lStrip  = 64
client = fastopc.FastOPC('localhost:7890')

pixels    = lib.Pixels(nStrips, lStrip, 0)
theo      = np.zeros([nStrips*lStrip, 3])

stream = micStream.Stream(fps=40, nBuffers=4)

powerSmooth = lib.ExpFilter(val=0.05, alpha_rise=0.05, alpha_decay=0.05)
nColorWheel = 300
colorWheel = lib.getColorWheel(nColorWheel)
frameCount = 0

while True:
    success = stream.readAndCalc()
    if success:
        frameNumEff = np.mod(frameCount, nColorWheel)
        power = np.sum(stream.freqSpectrum[10//5:300//5])
        powerSmooth.update(power)
        displayPower = int(122*power/powerSmooth.value)
        theoStrip = np.roll(theoStrip, 1, axis=0)
        theoStrip[0] = displayPower * colorWheel[frameNumEff]
        pixels.update(theoStrip, 1.0, 0.5)
        #print(displayPower * colorWheel[frameNumEff])
        client.putPixels(0, pixels.getArrayForDisplay())
        frameCount+=1
