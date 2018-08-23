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
nOnOneStrip = 20
colorWheel = lib.getColorWheel(nColorWheel)
frameCount = 0

while True:
    success = stream.readAndCalc()
    if success:
        frameNumEff  = np.mod(frameCount, nColorWheel)
        frameNumEff2 = np.mod(frameCount, nOnOneStrip*nStrips//2)
        stripNum     = np.mod(frameNumEff, nStrips//2)
        power = np.sum(stream.freqSpectrum[10//5:300//5])
        powerSmooth.update(power)
        displayPower = int(122*power/powerSmooth.value)
        
        theo = np.roll(theo, 1, axis=0)
        
        for i in range(nStrips):
            theo[i*lStrip + 63] = [0,0,0]

        theo[stripNum*2*lStrip] = displayPower * colorWheel[frameNumEff]
        theo[stripNum*2*lStrip + lStrip] = displayPower * colorWheel[frameNumEff]
        
        pixels.update(theoStrip, 1.0, 1.0)
        #print(displayPower * colorWheel[frameNumEff])
        client.putPixels(0, pixels.getArrayForDisplay())
        frameCount+=1