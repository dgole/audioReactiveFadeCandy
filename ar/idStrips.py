#!/usr/bin/env python

import fastopc, time
import numpy as np
import functionLib as lib

nStrips = 8
lStrip  = 64
client = fastopc.FastOPC('localhost:7890')

pixels = lib.Pixels(nStrips, lStrip, 0)

theo = np.zeros_like(pixels.array)
for i in range(0, nStrips):
    base=lStrip*i
    theo[base:base+i+1]  = [0,0,255]

while True:
    pixels.update(theo, 1.0, 1.0)
    client.putPixels(0, pixels.getArrayForDisplay())
    time.sleep(1)
    client.putPixels(0, np.zeros_like(pixels.getArrayForDisplay()))
    time.sleep(1)
