#!/usr/bin/env python

import fastopc, time
import numpy as np
import functionLib as lib
import micStream

nStrips = 16
lStrip  = 64
#client = fastopc.FastOPC('localhost:7890')

pixels    = lib.Pixels(nStrips, lStrip, 0)
theoStrip = np.zeros([lStrip, 3])

stream = micStream.Stream(fps=40, nBuffers=4)

powerSmooth = lib.ExpFilter(val=0.05, alpha_rise=0.05, alpha_decay=0.05)

while True:
    success = stream.readAndCalc()
    if success: 
        power = np.sum(stream.freqSpectrum[10//5:300//5])
        powerSmooth.update(power)
        displayPower = int(100*power/powerSmooth.value)
        theoStrip[:,0] = displayPower
        pixels.update(theoStrip, 0.9, 0.2)
        print(displayPower)
        #client.putPixels(0, pixels.getArrayForDisplay())
