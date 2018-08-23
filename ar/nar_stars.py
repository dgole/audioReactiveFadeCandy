#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np
import functionLib as lib

nStrips = 16
lStrip  = 64

client = fastopc.FastOPC('localhost:7890')

nStars = 200
pixels = lib.Pixels(nStrips, lStrip, 0)
theoStrips = np.zeros([nStars, nStrips*lStrip, 3])
zeroStrip = np.zeros_like(pixels.getArrayForDisplay())

while True:
    # select new values
    positions = np.random.randint(0, high=nStrips*lStrip-1, size=nStars)
    colors    = np.random.randint(0, 255, size=[nStars,3])
    for n in range(nStars): theoStrips[n, positions[n]] = colors[n] 
    # bring in new stars
    for i in range(0,nStars*50):
        starNum = np.floor(i/100)
        print(starNum)
        pixels.update(theoStrips[starNum], 0.05, 0.0)
        client.putPixels(0, pixels.getArrayForDisplay())
    # clear old stars
    for i in range(0,500):
        pixels.update(zeroStrip, 0.0, 0.02)
        client.putPixels(0, pixels.getArrayForDisplay())
    # fully zero out strip
    pixels.update(zeroStrip, 1.0, 1.0)
