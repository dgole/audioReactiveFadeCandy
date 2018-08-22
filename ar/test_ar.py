#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np
import functionLib as lib
import micStream

nStrips = 16
lStrip  = 64
client = fastopc.FastOPC('localhost:7890')

pixels = Pixels(nStrips, lStrip, 20)
theo = np.zeros_like(pixels.array)

stream = micStream.Stream()

while True:
    stream.readAndCalculate()
	pixels.update(arrayTheo, 1.0, 0.0)
	client.putPixels(0, pixels.getArrayForDisplay())
	time.sleep(1)
	client.putPixels(0, np.zeros_like(pixels.getArrayForDisplay()))
	time.sleep(1)
