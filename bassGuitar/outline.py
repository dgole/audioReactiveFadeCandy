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
theoAll   =
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
        frameNumEff = np.mod(frameCount, nColorWheel)
        power = np.sum(stream.freqSpectrum[20//7:250//7])
        powerSmooth.update(power)
        theoNeck     = np.roll(theoNeck, 1, axis=0)
        theoNeck[0]  = displayPower * colorWheel[frameNumEff]
        theoBody     = displayPower * colorWheel[np.mod(frameNumEff+200, nColorWheel)]
        pixels.updateBody(theoBody, 0.5, 0.5)
        pixels.updateNeck(theoNeck, 0.5, 0.5)
        print(displayPower * colorWheel[frameNumEff])
        #client.putPixels(0, brightnessFactor*pixels.getArrayForDisplay())
        frameCount+=1
