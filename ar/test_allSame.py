#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np

nStrips = 8
lStrip  = 64

client = fastopc.FastOPC('localhost:7890')

n = 1
dir = 1
pixels = Pixels(nStrips, lStrip, 20)
theoStrip = np.zeros([lStrip,3])
color=2
theoStrip[n,color] = 255

while True:
    if n == (64-1):
        dir *=-1
    elif n == 0:
		dir*=-1
		theoStrip=np.roll(theoStrip, 1, axis=1)
	theoStrip = np.roll(theoStrip, dir, axis=0)
	pixels.update(theoStrip, 0.7, 0.1)
	client.putPixels(0, pixels.getArrayForDisplay())
	n+=dir
	time.sleep(0.005)
