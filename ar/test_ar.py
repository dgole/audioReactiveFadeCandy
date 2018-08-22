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

theoStrip[:,2] = 200
pixels.update(theoStrip, 0.5, 0.1)
client.putPixels(0, pixels.getArrayForDisplay())

stream = micStream.Stream(fps=5, nBuffers=1)
print(stream.fps)

while True:
    success = stream.readAndCalc()
    if success: 
        power = stream.noteSpectrum[10]
        print(power)
        time.sleep(0.1)
