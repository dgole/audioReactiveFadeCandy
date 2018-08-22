#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np
import functionLib as lib
import micStream

nStrips = 16
lStrip  = 64
client = fastopc.FastOPC('localhost:7890')

pixels    = lib.Pixels(nStrips, lStrip, 20)
theoStrip = np.zeros([lStrip, 3])

stream = micStream.Stream()

while True:
    stream.readAndCalc()
    power = stream.noteSpectrum[10]
    print(power)
    theoStrip[:,2] = 100
    pixels.update(theoStrip, 0.5, 0.1)
    client.putPixels(0, pixels.getArrayForDisplay())
