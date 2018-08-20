#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np
import functionLib as lib

numLEDs = 512
client = fastopc.FastOPC('localhost:7890')

pixels = Pixels(numLEDs, 20)
arrayTheo = np.zeros_like(pixels.array)
for i in range(0,8):
	base=64*i
	arrayTheo[base:base+i+1]  = [0,0,255]

while True:
	pixels.update(arrayTheo, 1.0, 0.0)
	client.putPixels(0, pixels.getArrayForDisplay())
	time.sleep(1)
	client.putPixels(0, np.zeros_like(pixels.getArrayForDisplay()))
	time.sleep(1)
