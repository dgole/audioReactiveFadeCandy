#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np
import functionLib as lib
import sys

if len(sys.argv) == 1: 
    brightnessFactor = 0.5
    colorOption = "all"
elif len(sys.argv) == 2: 
    brightnessFactor = float(sys.argv[1])
    colorOption = "all"
else: 
    brightnessFactor = float(sys.argv[1])
    colorOption = str(sys.argv[2])

    
nStrips = 16
lStrip  = 64

client = fastopc.FastOPC('localhost:7890')

waitTime = 0.1
#fade stars in over 10 frames at 0.1 s/frame is 1s per star

nStars = 70
pixels = lib.Pixels(nStrips, lStrip, 0)
theoStrips = np.zeros([nStars, nStrips*lStrip, 3])
zeroStrip = np.zeros_like(pixels.getArrayForDisplay())
client.putPixels(0, zeroStrip)

while True:
    # select new values
    positions = np.random.randint(0, high=nStrips*lStrip-1, size=nStars)
    colors    = np.random.randint(0, 255, size=[nStars,3])
    for n in range(nStars):
        maxColor  = np.amax(colors[n])
        if colorOption == "all":
            colors[n]    = 255*colors[n]/maxColor
        elif colorOption=="red":
            colors[n] = [255,0,0]
        elif colorOption=="blue":
            colors[n] = [0,0,255]
        elif colorOption=="green":
            colors[n] = [0,255,0]
        elif colorOption=="purple":
            colors[n] = [200,0,150]
    for n in range(nStars): theoStrips[n, positions[n]] = colors[n] 
    # bring in new stars
    for i in range(0,nStars*10):
        starNum = np.floor(i/10)
        pixels.update(theoStrips[starNum], 0.2, 0.0)
        if np.sum(pixels.getArrayForDisplay()) > (1024*3*200):
            client.putPixels(0, np.zeros_like(pixels.getArrayForDisplay()))
            break
        else:
            client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        time.sleep(waitTime)
    # clear old stars
    for i in range(0,int(20/waitTime)):
        pixels.update(zeroStrip, 0.0, 0.02)
        client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        time.sleep(waitTime)
    # fully zero out strip
    pixels.update(zeroStrip, 1.0, 1.0)
