# start with 4 strips
# 1. around body (40 leds)
# 2. along neck top (20 leds)
# 3. along neck bottom (20 leds)
# 4. along strap (40ish)
# 4 fadecandy channels
# that's about 120 leds total
# 120 * 20 mA per color led = 2.4 A, exactly max for battery.
# dial fadecandy whitepoint to 0.8 or so and we're good to max out 1 color.
#
# MODE IDEAS
# body brightness all same, scales with volume.  number of lights lit on neck scales with volume.
#

#!/usr/bin/env python

import numpy as np
import sys
sys.path.append("../ar/")
import fastopc, time
import functionLib as lib
import micStream

if len(sys.argv) == 1: brightnessFactor = 0.6
else: brightnessFactor = float(sys.argv[1])

lNeck  = 18
lBody  = 40
lStrap = 36

pixels    = lib.BassPixels(lNeck, lBody, lStrap, 0)
theoNeck1 = np.zeros([lNeck,  3])
theoNeck2 = np.zeros([lNeck,  3])
theoBody  = np.zeros([lBody,  3])
theoStrap = np.zeros([lStrap, 3])

nColorWheel = 600
colorWheel = lib.getColorWheel(nColorWheel)
frameCount = 0

while True:
    success = stream.readAndCalc()
    if success:
        frameNumEff   = np.mod(frameCount, nColorWheel)
        theoNeck1     = np.roll(theoNeck1, 1, axis=0)
        theoNeck2     = np.roll(theoNeck2, 1, axis=0)
        theoBody      = np.roll(theoBody,  1, axis=0)
        theoStrap     = np.roll(theoStrap, 1, axis=0)
        theoNeck[0]  = displayPower * colorWheel[frameNumEff]
        theoBody     = displayPower * colorWheel[np.mod(frameNumEff+200, nColorWheel)]
        pixels.updateBody(theoBody, 0.5, 0.5)
        pixels.updateNeck(theoNeck, 0.5, 0.5)
        print(displayPower * colorWheel[frameNumEff])
        #client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        frameCount+=1

bouncerList = []
for i in range(4):
    bouncerList.append(Bouncer(np.random.randint(1,high=4), np.random.rand()*0.1+0.05, np.random.rand(3), 64))

while True:
    for i in range(0,nBouncers): bouncerList[i].update()
    for i in range(0,16):
        stripNum = i
        base = stripNum*lStrip
        theoStrip[base:base+lStrip] = bouncerList[i].getFullOutArray() + bouncerList[i+16].getFullOutArray()
    pixels.update(theoStrip, 0.5, 0.5)
    #print((pixels.getArrayForDisplay())[0:64,0])
    client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
    #time.sleep(0.01)
