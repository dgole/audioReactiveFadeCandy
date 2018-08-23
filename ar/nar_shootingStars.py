#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np
import functionLib as lib

nStrips = 16
lStrip  = 64

client = fastopc.FastOPC('localhost:7890')

pixels = lib.Pixels(nStrips, lStrip, 20)
zeroStrip = np.zeros_like(pixels.getArrayForDisplay())

chance = 0.05
waitBetweenChances = 0.05
waitTimeMultiplier = 0.01

while True:
    if np.random.rand()<chance:
        waitTimeThisStar = np.random.rand() * waitTimeMultiplier
        dir       = np.random.choice([-1,1])
        pos       = np.random.randint(1, high=lStrip-1)
        color     = np.random.randint(0, 255, size=3)
        theoStrip = zeroStrip
        theoStrip[pos] = color
        for i in range(0, 64):
            modNum = np.mod(pos, 128)
            if modNum == 0 or modNum == 63 or modNum == 64 or modNum == 127:
                pixels.update(zeroStrip, 1.0, 0.1)
            else:
                pos+=dir
                theoStrip = np.roll(theoStrip, dir, axis=0)
                pixels.update(theoStrip, 1.0, 0.1)
                if np.sum(pixels.getArrayForDisplay()) > (1024*3*200):
                    client.putPixels(0, np.zeros_like(pixels.getArrayForDisplay()))
                    break
                else:
                    client.putPixels(0, pixels.getArrayForDisplay())
                time.sleep(waitTimeThisStar)
    time.sleep(waitBetweenChances)

            
 

