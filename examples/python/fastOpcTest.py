#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import fastopc, time
import numpy as np

numLEDs = 512
client = fastopc.FastOPC('localhost:7890')

pixels = np.zeros([numLEDs, 3])

class Pixels():
	def __init__(self, numLEDs, floor):
		self.numLEDs = numLEDs
		self.floor = floor
		self.array = np.zeros([self.numLEDs, 3])
	def update(self, arrayNew, alphaRise, alphaDecay):
		alpha = arrayNew - self.array
		alpha[alpha > 0.0 ] = alphaRise
		alpha[alpha <= 0.0] = alphaDecay
		self.array = alpha*arrayNew + (1.0-alpha)*self.array
	def getArrayForDisplay(self):
		returnArray = self.array
		returnArray[returnArray < self.floor] = 0
		return returnArray
	

n = 1
dir = 1
pixels = Pixels(numLEDs, 20)
arrayTheo = np.zeros_like(pixels.array)
color=2
arrayTheo[n,color] = 255

while True:
	if n == (numLEDs-1):
		dir*=-1
	elif n == 0:
		dir*=-1
		arrayTheo=np.roll(arrayTheo, 1, axis=1)
	arrayTheo = np.roll(arrayTheo, dir, axis=0)
	pixels.update(arrayTheo, 0.7, 0.1)
	client.putPixels(0, pixels.getArrayForDisplay())
	n+=dir
	time.sleep(0.005)
