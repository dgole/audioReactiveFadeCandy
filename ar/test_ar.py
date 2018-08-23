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

theoStrip[:,2] = 100
pixels.update(theoStrip, 1.0, 0.1)
client.putPixels(0, pixels.getArrayForDisplay())

stream = micStream.Stream()

while True:
    success = stream.readAndCalc()
    if success:
        power = np.sum(stream.noteSpectrum[4:20]
        print(power)
