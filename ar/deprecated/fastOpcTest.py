#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np
import functionLib as lib

client = fastopc.FastOPC('localhost:7890')

n         = 1
dir       = 1
pixels    = lib.Pixels(1, 64, 0)
arrayTheo = np.zeros_like(pixels.array)
color     = 2
arrayTheo[n,color] = 255

while True:
	if n == (64-1):
		dir*=-1
	elif n == 0:
		dir*=-1
		arrayTheo=np.roll(arrayTheo, 1, axis=1)
	arrayTheo = np.roll(arrayTheo, dir, axis=0)
	pixels.update(arrayTheo, 0.7, 0.1)
	client.putPixels(0, pixels.getArrayForDisplay())
	n+=dir
	time.sleep(0.005)
