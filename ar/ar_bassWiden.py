#!/usr/bin/env python

import fastopc, time
import numpy as np
import functionLib as lib
import micStream

nStrips = 16
lStrip  = 64
client = fastopc.FastOPC('localhost:7890')

pixels    = lib.Pixels(nStrips, lStrip, 0)
theoStrip = np.zeros([lStrip, 3])

stream = micStream.Stream(fps=40, nBuffers=4)

powerSmooth = lib.ExpFilter(val=0.05, alpha_rise=0.05, alpha_decay=0.05)
nColorWheel = 1500
colorWheel = lib.getColorWheel(nColorWheel)
frameCount = 0

while True:
    success = stream.readAndCalc()
    if success:
        frameNumEff = np.mod(frameCount, nColorWheel)
        power = np.sum(stream.freqSpectrum[10//5:200//5])
        powerSmooth.update(power)
        displayPower = int(122*power/powerSmooth.value)       
        width = int(5 + np.sqrt(float(displayPower)))
        theoStrip[0:width] =  255 * colorWheel[frameNumEff-nColorWheel//2]
        theoStrip[width:]  = displayPower * colorWheel[frameNumEff]
        pixels.update(theoStrip, 0.7, 0.1)
        print(width)
        print(displayPower * colorWheel[frameNumEff])
        if np.sum(pixels.getArrayForDisplay()) > (1024*3*200):
            client.putPixels(0, np.zeros_like(pixels.getArrayForDisplay()))
            break
        else:
            client.putPixels(0, pixels.getArrayForDisplay())
            frameCount+=1
