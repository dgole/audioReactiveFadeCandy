#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np
import functionLib as lib

nStrips = 16
lStrip  = 64

client = fastopc.FastOPC('localhost:7890')

n = 1
dir = 1
pixels = lib.Pixels(nStrips, lStrip, 20)
theoStrip = np.zeros([lStrip*nStrips,3])
color=2
theoStrip[n,color] = 255

while True:
    if n == (nStrips*lStrip-1):
        dir *=-1
    elif n == 0:
        dir*=-1
        theoStrip=np.roll(theoStrip, 1, axis=1)
    theoStrip = np.roll(theoStrip, dir, axis=0)
    pixels.update(theoStrip, 1.0, 0.0025)
    client.putPixels(0, pixels.getArrayForDisplay())
    n+=dir
    #time.sleep(0.001)
