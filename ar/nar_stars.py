#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np
import functionLib as lib

nStrips = 16
lStrip  = 64

#client = fastopc.FastOPC('localhost:7890')

nStars = 50
pixels = lib.Pixels(nStrips, lStrip, 0)
theoStrips = np.zeros([nStars, nStrips*lStrip, 3])


while True:
    positions = np.random.randint(0, high=nStrips*lStrip-1, size=nStars)
    colors    = np.random.randint(50, 255, size=[nStars,3])
    for n in range(nStars): theoStrips[n, positions[n]] = colors[n] 
    for i in range(0,nStars*100):
        starNum = np.floor(i/100)
        pixels.update(theoStrips[starNum], 0.05, 0.0)
        #client.putPixels(0, pixels.getArrayForDisplay())
        print(pixels.getArrayForDisplay())
        time.sleep(0.1)
