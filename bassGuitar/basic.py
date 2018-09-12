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

client = fastopc.FastOPC('localhost:7890')

lNeck  = 18
lBody  = 40
lStrap = 36

pixels    = lib.BassPixels(lNeck, lBody, lStrap, 0)
theoNeck  = np.zeros([lNeck,  3])
theoBody  = np.zeros([lBody,  3])
theoStrap = np.zeros([lStrap, 3])

stream = micStream.Stream(fps=30, nBuffers=4)

powerSmooth = lib.ExpFilter(val=0.05, alpha_rise=0.05, alpha_decay=0.05)
nColorWheel = 600
colorWheel = lib.getColorWheel(nColorWheel)
frameCount = 0

breakVar=0
while breakVar==0:
    success = stream.readAndCalc()
    if success:
        frameNumEff = np.mod(frameCount, nColorWheel)
        power = np.sum(stream.freqSpectrum[20//7:250//7])
        powerSmooth.update(power)
        displayPower = int(122*power/powerSmooth.value)
        width = int(5 + np.sqrt(float(displayPower)))
        theoBody          = displayPower * colorWheel[np.mod(frameNumEff+200, nColorWheel)]
        theoNeck[0:width] = 255          * colorWheel[np.mod(frameNumEff,     nColorWheel)]
        pixels.updateBody(theoBody, 0.7, 0.1)
        pixels.updateNeck(theoNeck, 0.7, 0.1)
        print(width)
        print(displayPower * colorWheel[frameNumEff])
        #client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        frameCount+=1
