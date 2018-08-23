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

while True:
    success = stream.readAndCalc()
    if success:
        power = np.sum(stream.freqSpectrum[30//5:120//5])
        print(power)
        print(stream.freqs)
        print(stream.notes)
        theoStrip[:,0] = power/1.0
        pixels.update(theoStrip, 0.9, 0.9)
        client.putPixels(0, pixels.getArrayForDisplay())
