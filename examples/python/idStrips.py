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
