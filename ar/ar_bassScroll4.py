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

stream = micStream.Stream(fps=30, nBuffers=4)

powerSmooth = lib.ExpFilter(val=0.05, alpha_rise=0.05, alpha_decay=0.05)
nColorWheel = 300
nOnOneStrip = 64
colorWheel = lib.getColorWheel(nColorWheel)
frameCount = 0

while True:
    success = stream.readAndCalc()
    if success:
        frameNumEff  = np.mod(frameCount, nColorWheel)
        stripNum     = np.mod(np.floor(frameNumEff/nOnOneStrip),nStrips//2)
        print(stripNum)
        power = np.sum(stream.freqSpectrum[20//7:250//7])
        powerSmooth.update(power)
        displayPower = int(122*np.power(power/powerSmooth.value,1.5))
        
        theo = np.roll(theo, 1, axis=0)
        
        for i in range(nStrips):
            theo[i*lStrip + 63] = [0,0,0]

        theo[stripNum*2*lStrip] = displayPower * colorWheel[frameNumEff]
        theo[stripNum*2*lStrip + lStrip] = displayPower * colorWheel[frameNumEff]
        
        pixels.update(theo, 1.0, 0.1)
        #print(displayPower * colorWheel[frameNumEff])
        client.putPixels(0, pixels.getArrayForDisplay())
        frameCount+=1
