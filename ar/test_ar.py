#!/usr/bin/env python

import fastopc, time
import numpy as np
import functionLib as lib
import micStream

nStrips = 16
lStrip  = 64
client = fastopc.FastOPC('localhost:7890')

pixels    = lib.Pixels(nStrips, lStrip, 20)
theoStrip = np.zeros([lStrip, 3])

stream = micStream.Stream(fps=10, nBuffers=1)

theoStrip[:,2] = 100
pixels.update(theoStrip, 0.5, 0.1)
client.putPixels(0, pixels.getArrayForDisplay())

while True:
    stream.readAndCalc()
    power = stream.noteSpectrum[10]
    print(power)
