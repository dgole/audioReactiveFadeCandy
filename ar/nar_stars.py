#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np
import functionLib as lib

nStrips = 16
lStrip  = 64

#client = fastopc.FastOPC('localhost:7890')

pixels = lib.Pixels(nStrips, lStrip, 20)
theoStrips = []
for n in range(100): 
    theoStrips.append(np.zeros_like(pixels.getArrayForDisplay))

nFrame = 0
while True:
    print(nFrame)
    pixels.update(theoStrip, 0.7, 0.0)
    #client.putPixels(0, pixels.getArrayForDisplay())
    nFrame+=1
    time.sleep(0.01)
