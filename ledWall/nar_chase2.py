#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import numpy as np
import sys
sys.path.append("../ar/")
import fastopc, time
import functionLib as lib
import micStream

if len(sys.argv) == 1: brightnessFactor = 1.0
else: brightnessFactor = float(sys.argv[1])

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
    theoStrip = np.roll(theoStrip, dir*129, axis=0)
    pixels.update(theoStrip, 1.0, 0.01)
    client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
    n+=dir
    time.sleep(0.01)
